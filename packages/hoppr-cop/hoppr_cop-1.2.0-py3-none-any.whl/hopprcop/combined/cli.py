"""A Vulnerability Scanner that combines results from all configured scanners.

--------------------------------------------------------------------------------
SPDX-FileCopyrightText: Copyright © 2022 Lockheed Martin <open.source@lmco.com>
SPDX-FileName: hopprcop/combined/cli.py
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

import traceback

from pathlib import Path

import typer

from typer import Typer

from hopprcop.combined.combined_scanner import CombinedScanner
from hopprcop.gemnasium.gemnasium_scanner import GemnasiumScanner
from hopprcop.grype.grype_scanner import GrypeScanner
from hopprcop.ossindex.oss_index_scanner import OSSIndexScanner
from hopprcop.reporting import Reporting
from hopprcop.reporting.models import ReportFormat
from hopprcop.trivy.trivy_scanner import TrivyScanner
from hopprcop.utils import parse_sbom, parse_sbom_json_string


app = Typer()


def _output_dir(output_dir: Path | None) -> Path:
    """Use `Path.cwd()` as output directory if not provided."""
    return output_dir or Path.cwd()


@app.command()
def vulnerability_report(
    bom: str = typer.Argument(None, help="the path to a cyclone-dx BOM"),
    formats: list[ReportFormat] = typer.Option([ReportFormat.TABLE], "--format", help="The report formats to generate"),
    output_dir: Path = typer.Option(None, callback=_output_dir, help="The directory where reports will be writen"),
    base_report_name: str = typer.Option(None, help="The base name supplied for the generated reports"),
    os_distro: str = typer.Option(
        None,
        help=(
            "The operating system distribution; this is important "
            "to ensure accurate reporting of OS vulnerabilities from grype. "
            "Examples include rhel:8.6 or rocky:9 "
        ),
        envvar="OS_DISTRIBUTION",
    ),
    trace: bool = typer.Option(False, help="Print traceback information on unhandled error"),
):
    """Generates vulnerability reports based on the specified BOM and formats."""
    try:
        if base_report_name is None:
            if bom.endswith(".json"):
                base_report_name = bom.removesuffix(".json")
            elif bom.endswith(".xml"):
                base_report_name = bom.removesuffix(".xml")
            else:
                base_report_name = "hoppr-cop-report"

        reporting = Reporting(output_dir, base_report_name)
        combined = CombinedScanner()
        grype_scanner = GrypeScanner()
        trivy_scanner = TrivyScanner()
        grype_scanner.grype_os_distro = os_distro
        trivy_scanner.trivy_os_distro = os_distro
        combined.set_scanners([grype_scanner, trivy_scanner, OSSIndexScanner(), GemnasiumScanner()])

        parsed_bom = None

        if bom.endswith((".json", ".xml")):
            if not Path(bom).exists():
                msg = typer.style(f"{bom} does not exist", fg=typer.colors.RED)
                typer.echo(msg)
                raise typer.Exit(code=1)

            parsed_bom = parse_sbom(Path(bom))
        else:
            parsed_bom = parse_sbom_json_string(bom, "The json provided sbom")

        results = combined.get_vulnerabilities_by_sbom(parsed_bom)
        reporting.generate_vulnerability_reports(formats, results, parsed_bom)
    except Exception as exc:
        if trace:
            typer.secho(traceback.format_exc(), fg=typer.colors.RED)

        typer.secho(message=f"unexpected error: {exc}", fg=typer.colors.RED)
