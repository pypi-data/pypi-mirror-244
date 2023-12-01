"""A Vulnerability Scanner for Gitlab's Gemnasiumm Database.

--------------------------------------------------------------------------------
SPDX-FileCopyrightText: Copyright © 2022 Lockheed Martin <open.source@lmco.com>
SPDX-FileName: hopprcop/gemnasium/gemnasium_scanner.py
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

import os
import pkgutil
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import zipfile

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar
from urllib.parse import urlparse

import requests
import typer
import yaml

from cvss import CVSS2, CVSS3
from hoppr import Vulnerability, cdx

from hopprcop.gemnasium.models import GemnasiumVulnerability
from hopprcop.utils import (
    get_advisories_from_urls,
    get_references_from_ids,
    get_vulnerability_source,
)
from hopprcop.vulnerability_scanner import VulnerabilitySuper


if TYPE_CHECKING:
    from packageurl import PackageURL


class GemnasiumScanner(VulnerabilitySuper):
    """A Vulnerability Scanner for Gitlab's Gemnasiumm Database."""

    supported_formats: ClassVar[list[str]] = ["npm", "maven", "pypi", "gem", "golang", "conan", "nuget"]
    # TODO: supported_formats is not used; should get_vulnerabilities_by_purl be filtering purls by it?

    url = os.getenv(
        "GEMNASIUM_DATABASE_ZIP",
        "https://gitlab.com/gitlab-org/advisories-community/-/archive/main/advisories-community-main.zip",
    )

    semver_path = Path("/usr/local/bin/semver")
    required_tools_on_path: ClassVar[list[str]] = ["ruby"]

    def __init__(self):
        self.database_path = self._get_cache_dir() / "gemnasium"

        if self.should_activate():
            if not self.semver_path.exists():
                self._extract_semver_to_local()

            self._download_and_extract_database()

    def _extract_semver_to_local(self):
        """If the ruby semver command isn't installed then extract from this package."""
        data = pkgutil.get_data(__name__, "semver").decode("utf-8")
        self.semver_path = Path(tempfile.gettempdir()) / "semver"
        self.semver_path.write_text(data, encoding="utf-8")
        self.semver_path.chmod(mode=stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    def _download_and_extract_database(self):
        """Downloads the gymnasium database."""
        url = urlparse(self.url)

        path_to_zip_file = self._get_cache_dir() / Path(url.path).name

        def do_download_and_unpack():
            typer.echo(f"Updating Gemnasium database to {self.database_path}")
            request = requests.get(self.url, allow_redirects=True)
            path_to_zip_file.write_bytes(request.content)

            with zipfile.ZipFile(path_to_zip_file, "r") as zip_ref:
                zip_ref.extractall(self.database_path)

        if not path_to_zip_file.exists():
            do_download_and_unpack()
        else:
            file_time = path_to_zip_file.stat().st_mtime
            # Check against 24 hours
            older_than_one_day = (time.time() - file_time) / 3600 > 24 * 1

            if older_than_one_day:
                shutil.rmtree(self.database_path / path_to_zip_file.stem)
                do_download_and_unpack()

        self.database_path = self.database_path / path_to_zip_file.stem

    def _is_affected_range(self, repository_format: str, version: str, affected_range: str) -> bool:
        """Checks if the version matches the affected range based on package manager specific semantic versioning.

        :param repository_format:
        :param version:
        :param affected_range:
        :return:
        """
        try:
            # Gemnasium docs list nuget as supported, however no results are returned
            # nuget package-versioning is based on maven dependency version
            # specification. Below repository_format override allows nuget vuln discovery
            # https://learn.microsoft.com/en-us/nuget/concepts/package-versioning
            # https://maven.apache.org/pom.html#dependency-version-requirement-specification
            repository_format = repository_format.replace("nuget", "maven")

            _win32 = sys.platform == "win32"
            output = subprocess.run(
                [
                    *(["ruby"] if _win32 else []),
                    self.semver_path,
                    "check_version",
                    repository_format,
                    version,
                    affected_range,
                ],
                capture_output=True,
                text=True,
                check=False,
                # TODO this command suddenly started throwing errors, not sure what changed but it needs investigated.
                # It looks like  a spell checker package changed
            )
            return "matches" in str(output)
        except Exception as err:
            typer.echo(f"Failed to check version for: {repository_format} {version} {err}")
            return False

    def get_vulnerabilities_by_purl(self, purls: list[PackageURL]) -> dict[str, list[cdx.Vulnerability]]:
        """Get the vulnerabilities for a list of package URLS (purls).

        Returns a dictionary of package URL to vulnerabilities or none if no vulnerabilities are found.
        """
        vulnerabilities_by_purl: dict[str, list[Vulnerability]] = {}
        for purl in purls:
            purl_str = purl.to_string()
            vulnerabilities_by_purl[purl_str] = []

            if not (path := self._get_path(purl)).exists():
                continue

            vuln_files = [file for file in path.glob("*") if file.is_file()]

            for vuln_file in vuln_files:
                try:
                    data = yaml.full_load(vuln_file.read_text(encoding="utf-8"))
                    vuln = GemnasiumVulnerability(**data)

                    if self._is_affected_range(purl.type, purl.version, vuln.affected_range):
                        vulnerability = self._convert_to_cyclone_dx(vuln)

                        if vulnerability.ratings:
                            vulnerabilities_by_purl[purl_str].append(vulnerability)
                except Exception:
                    typer.echo(f"failed to parse gemnasium file for {purl}")

        return vulnerabilities_by_purl

    @staticmethod
    def _convert_to_cyclone_dx(vuln: GemnasiumVulnerability) -> Vulnerability:
        """Converts a gemnasium vulnerabity to a vulnerability."""
        res = list(filter(lambda x: "cve-" in x.lower(), vuln.identifiers))
        vuln_id = res[0] if len(res) > 1 else vuln.identifiers[0]
        cwes = []

        if vuln.cwe_ids is not None:
            cwes = [int(x.replace("CWE-", "")) for x in vuln.cwe_ids]

        cyclone_vuln = Vulnerability(
            id=vuln_id,
            recommendation=vuln.solution,
            cwes=cwes,
            description=vuln.description,
            ratings=[],
            source=get_vulnerability_source(vuln_id),
        )

        cyclone_vuln.advisories = get_advisories_from_urls(vuln.urls)
        cyclone_vuln.references = get_references_from_ids(vuln.identifiers, cyclone_vuln.id)

        if vuln.cvss_v3 is not None:
            cvss = CVSS3(vuln.cvss_v3)
            cyclone_vuln.ratings.append(
                cdx.Rating(
                    score=cvss.base_score,
                    severity=cdx.Severity[cvss.severities()[0].lower()],
                    method=cdx.ScoreMethod.CVSSv3,
                    vector=str(cvss.clean_vector()),
                )
            )
        elif vuln.cvss_v2 is not None:
            cvss = CVSS2(vuln.cvss_v2)
            cyclone_vuln.ratings.append(
                cdx.Rating(
                    score=cvss.base_score,
                    severity=cdx.Severity[cvss.severities()[0].lower()],
                    method=cdx.ScoreMethod.CVSSv2,
                    vector=cvss.clean_vector(),
                )
            )

        cyclone_vuln.tools = [cdx.Tool(vendor="Gitlab", name="Gemnasium")]

        return cyclone_vuln

    @staticmethod
    def _get_cache_dir() -> Path:
        cache = os.getenv("CACHE_DIR")
        return Path(cache) if cache is not None else Path(tempfile.gettempdir())

    def _get_path(self, purl: PackageURL) -> Path:
        """Build a path to the gemnasium path."""
        repo_format = purl.type
        namespace = purl.namespace or ""

        if repo_format == "npm":
            path_slug = Path("npm") / namespace / purl.name
        elif repo_format == "maven":
            path_slug = Path("maven") / namespace / purl.name
        elif repo_format == "golang":
            path_slug = Path("go") / namespace / purl.name
        else:
            path_slug = Path(repo_format) / purl.name

        return self.database_path / path_slug
