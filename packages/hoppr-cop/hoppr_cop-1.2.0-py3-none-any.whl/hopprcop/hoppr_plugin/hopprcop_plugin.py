"""Setup hoppr-cop as a plugin for hoppr.

--------------------------------------------------------------------------------
SPDX-FileCopyrightText: Copyright © 2022 Lockheed Martin <open.source@lmco.com>
SPDX-FileName: hopprcop/hoppr_plugin/hopprcop_plugin.py
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

import uuid

from copy import deepcopy
from pathlib import Path

from hoppr import Affect, BomAccess, Component, HopprPlugin, Result, Sbom, Vulnerability, hoppr_process

from hopprcop import __version__
from hopprcop.combined.combined_scanner import CombinedScanner
from hopprcop.reporting import Reporting
from hopprcop.reporting.models import ReportFormat
from hopprcop.vulnerability_combiner import combine_vulnerabilities


class HopprCopPlugin(HopprPlugin):
    """hoppr plugin wrapper for hopprcop integration."""

    class ComponentVulnerabilityWrapper:
        """Wrapper for the vulnerabilities associated with a component."""

        def __init__(
            self,
            serial_number: str | None = None,
            version: str | None = None,
            vulnerabilities: dict[str, list[Vulnerability]] | None = None,
        ):
            self.serial_number = serial_number
            self.version = version
            self.vulnerabilities = vulnerabilities

    EMBEDDED_VEX = "embedded_cyclone_dx_vex"
    LINKED_VEX = "linked_cyclone_dx_vex"

    bom_access = BomAccess.FULL_ACCESS

    def get_version(self) -> str:
        """__version__ required for all HopprPlugin implementations."""
        return __version__

    @hoppr_process
    def pre_stage_process(self) -> Result:
        """Supply sbom to hoppr cop to perform vulnerabilty check."""
        self.get_logger().info("[ Executing hopprcop vulnerability check ]")

        self.config = self.config or {}
        output_dir = Path(self.config.get("output_dir", self.context.collect_root_dir / "generic"))
        base_report_name = self.config.get("base_report_name", "hopprcop-vulnerability-results")
        scanners = self.config.get("scanners", get_scanners())
        formats = self.config.get("result_formats", [self.EMBEDDED_VEX])

        output_dir.mkdir(parents=True, exist_ok=True)

        reporting = Reporting(output_dir, base_report_name)
        combined = CombinedScanner()
        combined.set_scanners(scanners)
        parsed_bom = self.context.delivered_sbom

        results = combined.get_vulnerabilities_by_sbom(parsed_bom)

        # Map bom ref to results - uses purl as ref
        bom_ref_to_results: dict[str, HopprCopPlugin.ComponentVulnerabilityWrapper] = {}

        # Map purls to components, try to normalize purls to lowercase
        purl_to_component = {component.purl.lower(): component for component in parsed_bom.components if component.purl}

        # Delivered Bom version
        bom_version = 1 if parsed_bom.version is not None else parsed_bom.version

        # Generate Delivered Bom Serial Number if it doesn't exist
        *_, bom_serial_number = (parsed_bom.serialNumber or uuid.uuid4().urn).split(":")

        parsed_bom.serialNumber = f"urn:uuid:{bom_serial_number}"
        parsed_bom.vulnerabilities = [] if parsed_bom.vulnerabilities is None else parsed_bom.vulnerabilities

        # Build dictionary to go from bom-ref to vulnerabilities
        for purl in results:
            # Different purl values being returned from different scanners, attempt to normalize the data
            # by making it lower case and if not found, reversing pypi expectations with - to _.
            adjusted_purl = purl.lower()
            if adjusted_purl not in purl_to_component and "pypi" in adjusted_purl:
                adjusted_purl = adjusted_purl.replace("-", "_")

            if adjusted_purl in purl_to_component:
                component = purl_to_component[adjusted_purl]
                bom_ref = component.purl  # component.bom_ref
                if len(parsed_bom.vulnerabilities) > 0 and bom_ref not in bom_ref_to_results:
                    # Account for existing vulnerabilites on bom
                    for existing_vulnerability in parsed_bom.vulnerabilities:
                        for affect in existing_vulnerability.affects:
                            if affect.ref in {bom_ref, component.bom_ref}:
                                results[purl].append(existing_vulnerability)

                    results[purl] = combine_vulnerabilities([{purl: results[purl]}])[0]

                updated_results = deepcopy(results[purl])

                if bom_ref not in bom_ref_to_results:
                    wrapper = self.ComponentVulnerabilityWrapper(bom_serial_number, bom_version, updated_results)
                    bom_ref_to_results[bom_ref] = wrapper
                elif len(bom_ref_to_results[bom_ref].vulnerabilities) > 0 and len(updated_results) > 0:
                    existing_vulnerabilities: list[Vulnerability] = bom_ref_to_results[bom_ref].vulnerabilities
                    bom_ref_to_results[bom_ref].vulnerabilities = combine_vulnerabilities(
                        [{purl: updated_results + existing_vulnerabilities}]
                    )[0]
            else:
                self.get_logger().info(f"Could not find purl ({purl}) in component map")

        hoppr_delivered_bom = self.__perform_hoppr_bom_updates(
            reporting, deepcopy(parsed_bom), bom_ref_to_results, formats
        )
        self.__perform_hopprcop_reporting(reporting, parsed_bom, results, formats)

        self.get_logger().flush()

        return Result.success(return_obj=hoppr_delivered_bom)

    def __add_bom_ref_and_flatten(
        self,
        reporting: Reporting,
        bom_ref_to_component: dict[str, list[Component]],
        external_ref: bool = False,
    ) -> list[Vulnerability]:
        flattened_vulnerabilities: list[Vulnerability] = []
        # Capture vulnerability id to vulnerability to account multiple components affected by the same vulnerability
        vuln_id_to_vuln = {}
        for bom_ref in bom_ref_to_component:
            for vuln in bom_ref_to_component[bom_ref].vulnerabilities:
                existing_vuln = vuln
                if existing_vuln.id not in vuln_id_to_vuln:
                    existing_vuln.affects = []
                else:
                    existing_vuln = vuln_id_to_vuln[vuln.id]

                if external_ref:
                    existing_vuln.affects.append(
                        Affect(
                            ref=f"urn:cdx:{bom_ref_to_component[bom_ref].serial_number}/{bom_ref_to_component[bom_ref].version}#{bom_ref}"
                        )
                    )
                else:
                    existing_vuln.affects.append(Affect(ref=bom_ref))

                vuln_id_to_vuln[vuln.id] = existing_vuln

        flattened_vulnerabilities = list(vuln_id_to_vuln.values())
        flattened_vulnerabilities.sort(key=reporting.get_score, reverse=True)

        return flattened_vulnerabilities

    def __perform_hoppr_bom_updates(
        self,
        reporting: Reporting,
        parsed_bom: Sbom,
        bom_ref_to_results: dict[str, ComponentVulnerabilityWrapper],
        formats: str,
    ) -> Sbom:
        if self.EMBEDDED_VEX in formats:
            flattened_results = self.__add_bom_ref_and_flatten(reporting, bom_ref_to_results)
            # Existing vulnerabilities were accounted for
            parsed_bom.vulnerabilities = []
            Reporting.add_vulnerabilities_to_bom(parsed_bom, flattened_results)
        elif self.LINKED_VEX in formats:
            flattened_results = self.__add_bom_ref_and_flatten(reporting, bom_ref_to_results, True)
            # Existing vulnerabilities were accounted for
            parsed_bom.vulnerabilities = []
            vex_bom = Reporting.link_vulnerabilities_to_bom(flattened_results)

            (reporting.output_path / f"{reporting.base_name}-vex.json").write_text(vex_bom.json())

        return parsed_bom

    def __perform_hopprcop_reporting(
        self,
        reporting: Reporting,
        parsed_bom: Sbom,
        results: dict[str, list[Vulnerability]],
        formats: list[str],
    ):
        if filtered_formats := list(filter(lambda fmt: fmt not in {self.LINKED_VEX, self.EMBEDDED_VEX}, formats)):
            filtered_formats = [ReportFormat[format.upper()] for format in filtered_formats]
            reporting.generate_vulnerability_reports(filtered_formats, results, parsed_bom)


def get_scanners() -> list[str]:
    """Defines scanners to use for hoppr cop."""
    return [
        "hopprcop.gemnasium.gemnasium_scanner.GemnasiumScanner",
        "hopprcop.grype.grype_scanner.GrypeScanner",
        "hopprcop.trivy.trivy_scanner.TrivyScanner",
        "hopprcop.ossindex.oss_index_scanner.OSSIndexScanner",
    ]
