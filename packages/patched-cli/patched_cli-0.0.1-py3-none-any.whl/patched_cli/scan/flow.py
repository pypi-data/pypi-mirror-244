from typing import Literal

from patched_cli.client.patched import PatchedClient
from patched_cli.models.common import VulnFile
from patched_cli.scan import semgrep_flow


def apply_flow(path: str, flow: Literal["semgrep"] | Literal["sonar"], vuln_file: str | None,
               client: PatchedClient) -> list[VulnFile]:

    src_with_vulns = []
    if flow == "semgrep":
        src_with_vulns = semgrep_flow.run(path, vuln_file)

    return src_with_vulns
