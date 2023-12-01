"""Scan an SBOM using the Trivy CLI.

--------------------------------------------------------------------------------
SPDX-FileCopyrightText: Copyright © 2022 Lockheed Martin <open.source@lmco.com>
SPDX-FileName: hopprcop/trivy/trivy_scanner.py
SPDX-FileType: SOURCE
SPDX-License-Identifier: MIT
--------------------------------------------------------------------------------
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
--------------------------------------------------------------------------------
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

from pathlib import Path
from subprocess import PIPE, Popen
from typing import ClassVar

import typer

from hoppr import Component, HopprError, Sbom, Vulnerability, cdx
from packageurl import PackageURL

from hopprcop.utils import build_bom_dict_from_purls
from hopprcop.vulnerability_scanner import VulnerabilitySuper


class TrivyScanner(VulnerabilitySuper):
    """Interacts with the trivy cli to scan an sbom."""

    # used to store the operating system component discovered in the provided bom for generating the bom for trivy
    _os_component: Component | None = None

    trivy_os_distro = os.getenv("OS_DISTRIBUTION", None)

    required_tools_on_path: ClassVar[list[str]] = ["trivy"]
    supported_types: ClassVar[list[str]] = ["conan", "deb", "gem", "golang", "maven", "npm", "nuget", "pypi", "rpm"]

    def get_vulnerabilities_by_purl(self, purls: list[PackageURL]) -> dict[str, list[Vulnerability]]:
        """Get the vulnerabilities for a list of package URLS (purls).

        Returns a dictionary of package URL to vulnerabilities or none if no vulnerabilities are found.
        """
        results: dict[str, list[Vulnerability]] = {purl.to_string(): [] for purl in purls}

        if purls := list(filter(lambda x: x.type in self.supported_types, purls)):
            bom = build_bom_dict_from_purls(purls)
            self._add_operating_system_component(bom)

            _win32 = sys.platform == "win32"
            with tempfile.NamedTemporaryFile(mode="w+", delete=not _win32, encoding="utf-8") as bom_file:
                # Remove tools from metadata due to cyclonedx-go only having partial support for spec version 1.5 (as of 0.72.0)
                # TODO: roll back once full support is in cyclonedx-go
                parsed_bom = Sbom.parse_obj(bom)
                if parsed_bom.metadata:
                    parsed_bom.metadata.tools = None

                bom_file.write(parsed_bom.json())
                bom_file.flush()

                args = ["trivy", "sbom", "--format", "cyclonedx", str(bom_file.name)]
                cache = os.getenv("CACHE_DIR")

                if cache is not None:
                    args += ["--cache-dir", cache]

                with Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE, text=True) as process:
                    stdout, stderr = process.communicate()
                    if not stdout and stderr:
                        raise HopprError(f"{self.__class__.__name__} generated an exception: {stderr}")

                    if _win32:
                        bom_file.close()
                        Path(bom_file.name).unlink()

            bom_dict = json.loads(stdout)

            bom_dict["metadata"]["component"]["type"] = "application"
            bom_dict["metadata"]["component"]["name"] = "generated"

            trivy_result = Sbom.parse_obj(bom_dict)

            for vuln in trivy_result.vulnerabilities:
                for affect in vuln.affects:
                    affect_dict = affect.dict()
                    *_, purl_str = str(affect_dict["ref"]).split("#")
                    affect.ref = purl_str or affect.ref

                    if vuln.ratings is not None:
                        results.setdefault(affect_dict["ref"], [])
                        results[affect_dict["ref"]].append(vuln)

                vuln.tools = [cdx.Tool(vendor="Aquasec", name="Trivy")]

        return results

    def get_vulnerabilities_by_sbom(self, bom: Sbom) -> dict[str, list[Vulnerability]]:
        """Accepts a cyclone dx compatible BOM and returns a list of vulnerabilities.

        Returns a dictionary of package URL to vulnerabilities or none if no vulnerabilities are found.
        """
        purls: list[PackageURL] = []
        self._os_component = None

        for component in bom.components or []:
            if component.purl is not None and component.purl != "":
                purls.append(PackageURL.from_string(component.purl))

            if "operating_system" in str(component.dict()["type"]):
                self._os_component = component

        return self.get_vulnerabilities_by_purl(purls)

    def _add_operating_system_component(self, bom: dict):
        version = None
        distro = None

        if self.trivy_os_distro is not None:
            parts = self.trivy_os_distro.split(":")

            if len(parts) != 2:
                typer.echo(f"{self.trivy_os_distro} is an invalid distribution ")
            else:
                distro = parts[0]
                version = parts[1]
        elif self._os_component is not None:
            version = self._os_component.version
            distro = self._os_component.name

        if version is not None and distro is not None:
            component = {
                "bom-ref": "ab16d2bb-90f7-4049-96ce-8c473ba13bd2",
                "type": "operating-system",
                "name": distro,
                "version": version,
            }
            bom["components"].append(component)
