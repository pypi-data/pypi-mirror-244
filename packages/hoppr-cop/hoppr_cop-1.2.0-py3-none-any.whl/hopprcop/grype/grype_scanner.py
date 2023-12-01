"""Scan an SBOM using the Grype CLI.

--------------------------------------------------------------------------------
SPDX-FileCopyrightText: Copyright © 2022 Lockheed Martin <open.source@lmco.com>
SPDX-FileName: hopprcop/grype/grype_scanner.py
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

from subprocess import PIPE, Popen
from typing import ClassVar

import typer

from cvss import CVSS2, CVSS3
from hoppr import Sbom, Vulnerability, cdx
from packageurl import PackageURL

from hopprcop.grype.models import GrypeResult, Match, Vulnerability as GrypeVulnerability
from hopprcop.utils import (
    build_bom_from_purls,
    get_advisories_from_urls,
    get_references_from_ids,
    get_vulnerability_source,
)
from hopprcop.vulnerability_scanner import VulnerabilitySuper


class GrypeScanner(VulnerabilitySuper):
    """This scanner utilizes the anchore grype command line to gather vulnerabilities."""

    required_tools_on_path: ClassVar[list[str]] = ["grype"]
    grype_os_distro = os.getenv("OS_DISTRIBUTION", None)

    def __init__(self):
        super()

    def get_vulnerabilities_by_purl(
        self, purls: list[PackageURL]
    ) -> dict[str, list[Vulnerability]]:  # pragma: no cover
        """Get the vulnerabilities for a list of package URLS (purls).

        This function will return a dictionary of package URL to vulnerabilities or none if no vulnerabilities are found.
        """
        bom = build_bom_from_purls(purls)
        return self.get_vulnerabilities_by_sbom(bom)

    def get_vulnerabilities_by_sbom(self, bom: Sbom) -> dict[str, list[Vulnerability]]:
        """Get the vulnerabilities for a list of package URLS (purls).

        Returns a dictionary of package URL to vulnerabilities or none if no vulnerabilities are found.
        """
        args = ["grype", "--output", "json"]
        if self.grype_os_distro is not None:
            args += ["--distro", self.grype_os_distro]

        with Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE) as process:
            # Remove tools from metadata due to cyclonedx-go only having partial support for spec version 1.5 (as of 0.72.0)
            # TODO: roll back once full support is in cyclonedx-go
            parsed_bom = bom.copy(deep=True)
            if parsed_bom.metadata:
                parsed_bom.metadata.tools = None

            stdout_data = process.communicate(input=(bytes(parsed_bom.json(), "utf-8")))[0]
            result = GrypeResult(**json.loads(stdout_data))
            results: dict[str, list[Vulnerability]] = {}

        # Use a generator to get all of the component purls if they exist and intialize the results for the purl
        for pkg_url in [component.purl for component in bom.components if component.purl]:
            results[pkg_url] = []

        for match in list(result.matches):
            purl = PackageURL.from_string(match.artifact.purl)

            if purl.type != "npm" or purl.namespace != "@types":
                # Raise the error if `match.artifact.purl` is not already a key in the dict
                # This can occur when the `match.artifact.purl` is not in the `component.purl` above
                try:
                    # Append the Grype result information to the results dict at the purl key
                    results[match.artifact.purl].append(self._convert_to_cyclone_dx(match))
                except KeyError:
                    typer.secho(f"WARNING -- Match not found: {match.artifact.purl}", fg=typer.colors.YELLOW)

        return results

    @staticmethod
    def _convert_to_cyclone_dx(match: Match) -> Vulnerability:
        """Converts a match to a vulnerability."""
        related: GrypeVulnerability = next(
            (related_vuln for related_vuln in match.related_vulnerabilities if related_vuln.id.startswith("CVE")),
            (match.related_vulnerabilities[0] if match.related_vulnerabilities else match.vulnerability),
        )
        cyclone_vuln = Vulnerability(
            id=related.id,
            description=related.description,
            ratings=[],
            recommendation=(
                f"State: {match.vulnerability.fix.state} | "
                f"Fix Versions: {','.join(match.vulnerability.fix.versions)}"
            ),
            source=get_vulnerability_source(related.id),
        )

        ids = [match.vulnerability.id, *[x.id for x in match.related_vulnerabilities]]

        # Maintain cyclone_vul.source or initialize to empty VulnerabilitySource
        cyclone_vuln.source = cyclone_vuln.source or cdx.VulnerabilitySource()
        cyclone_vuln.source.url = related.data_source
        cyclone_vuln.advisories = get_advisories_from_urls(related.urls)
        cyclone_vuln.references = get_references_from_ids(ids, cyclone_vuln.id)
        cvss_scores = match.vulnerability.cvss or related.cvss
        for cvss in cvss_scores:
            if cvss.version.startswith("3"):
                cvss3 = CVSS3(cvss.vector)
                method = "CVSSv31" if cvss.version == "3.1" else "CVSSv3"

                cyclone_vuln.ratings.append(
                    cdx.Rating(
                        score=cvss3.base_score,
                        severity=cdx.Severity[cvss3.severities()[0].lower()],
                        method=cdx.ScoreMethod(method),
                        vector=cvss.vector,
                    )
                )
            elif cvss.version.startswith("2"):
                cvss2 = CVSS2(cvss.vector)

                cyclone_vuln.ratings.append(
                    cdx.Rating(
                        score=cvss2.base_score,
                        severity=cdx.Severity[cvss2.severities()[0].lower()],
                        method=cdx.ScoreMethod.CVSSv2,
                        vector=cvss.vector,
                    )
                )

        if not cyclone_vuln.ratings and match.vulnerability.severity:
            cyclone_vuln.ratings.append(
                cdx.Rating(
                    severity=cdx.Severity[match.vulnerability.severity.lower()],
                    method=cdx.ScoreMethod.OTHER,
                )
            )

        cyclone_vuln.tools = [cdx.Tool(vendor="Anchore", name="Grype")]

        return cyclone_vuln
