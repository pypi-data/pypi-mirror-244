"""A Vulnerability Scanner that combines results from all configured scanners.

--------------------------------------------------------------------------------
SPDX-FileCopyrightText: Copyright © 2022 Lockheed Martin <open.source@lmco.com>
SPDX-FileName: hopprcop/combined/combined_scanner.py
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

import concurrent.futures
import importlib

from typing import TYPE_CHECKING, ClassVar, cast

import typer

from rich.progress import Progress, SpinnerColumn, TextColumn

from hopprcop.vulnerability_combiner import combine_vulnerabilities
from hopprcop.vulnerability_scanner import VulnerabilitySuper


if TYPE_CHECKING:
    from collections.abc import Callable

    from hoppr import Sbom, Vulnerability
    from packageurl import PackageURL


class CombinedScanner(VulnerabilitySuper):
    """A Vulnerability Scanner that combines results from all configured scanners."""

    scanners: ClassVar[list[VulnerabilitySuper]] = []

    def set_scanners(self, scanners: list[VulnerabilitySuper] | list[str]):
        """Sets the scanners that should be used for vulnerability scanning.

        The argument can either be a list of scanner instances or a list of fully qualified strings to a scanner
        instance. For example ["vuln.gemnasium.gemnasium_scanner.GemnasiumScanner"].
        """
        for scanner in scanners:
            if isinstance(scanner, str):
                modname, _, clsname = scanner.rpartition(".")
                mod = importlib.import_module(modname)
                scanner = cast(VulnerabilitySuper, getattr(mod, clsname)())

            if scanner.should_activate():
                typer.echo(f"{scanner.__class__.__name__} is activated")
                self.scanners.append(scanner)

    def _scan_concurrently(self, function: Callable) -> dict[str, list[Vulnerability]]:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            results = []
            progress.add_task(description="Fetching vulnerabilities...", total=None)

            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                futures = {executor.submit(function, scanner): scanner for scanner in self.scanners}

            for future in concurrent.futures.as_completed(futures):
                scanner = futures[future]

                try:
                    scanner_results = future.result()
                    results.append(scanner_results)
                except Exception as exc:
                    typer.echo(f"{type(scanner).__name__} generated an exception: {exc}")

        return combine_vulnerabilities(list(results))

    def get_vulnerabilities_by_purl(
        self, purls: list[PackageURL]
    ) -> dict[str, list[Vulnerability]]:  # pragma: no cover
        """Get the vulnerabilities for a list of package URLS (purls).

        Returns a dictionary of package URL to vulnerabilities or none if no vulnerabilities are found.
        """

        def submit_to_scanner_purl(scanner: VulnerabilitySuper) -> dict[str, list[Vulnerability]]:
            return scanner.get_vulnerabilities_by_purl(purls)

        return self._scan_concurrently(submit_to_scanner_purl)

    def get_vulnerabilities_by_sbom(self, bom: Sbom) -> dict[str, list[Vulnerability]]:  # pragma: no cover
        """Parse a CycloneDX compatible BOM and return a list of vulnerabilities.

        Returns a dictionary of package URL to vulnerabilities or none if no vulnerabilities are found.
        """

        def submit_to_scanner(scanner: VulnerabilitySuper) -> dict[str, list[Vulnerability]]:
            return scanner.get_vulnerabilities_by_sbom(bom)

        return self._scan_concurrently(submit_to_scanner)
