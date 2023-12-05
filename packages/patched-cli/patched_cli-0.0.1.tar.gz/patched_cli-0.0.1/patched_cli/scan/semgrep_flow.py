import json
import subprocess
from collections import defaultdict
from typing import Dict, List

from patched_cli.models.common import Vuln, VulnFile


def run_semgrep(repo_directory: str) -> Dict:
    cmd = ["semgrep", "--config", "auto", "--config", "p/python", repo_directory, "--json"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(p.stdout)


def semgrep_to_vulns(semgrep_result) -> List[VulnFile]:
    semgrep_result = semgrep_result["results"]

    path_vulns = defaultdict(list)
    for result in semgrep_result:
        try:
            cwe = result["extra"]["metadata"]["cwe"]
        except KeyError:
            continue

        if isinstance(cwe, list):
            for cwe_element in cwe:
                vuln = Vuln(cwe=cwe_element,
                                     bug_msg=result["extra"]["message"],
                                     start=result["start"]["line"],
                                     end=result["end"]["line"])
                path_vulns[result["path"]].append(vuln)
        else:
            vuln = Vuln(cwe=cwe,
                                 bug_msg=result["extra"]["message"],
                                 start=result["start"]["line"],
                                 end=result["end"]["line"])
            path_vulns[result["path"]].append(vuln)

    vuln_files = []
    for path, vulns in path_vulns.items():
        with open(path, 'r') as src_file:
            src = src_file.read()
        vuln_file = VulnFile(path=path, src=src, vulns=vulns)
        vuln_files.append(vuln_file)
    return vuln_files


def run(path: str, vuln_file: str | None) -> List[VulnFile]:
    if vuln_file is None:
        semgrep_result = run_semgrep(path)
    else:
        with open(vuln_file, "r") as f:
            semgrep_result = json.load(f)
    return semgrep_to_vulns(semgrep_result)
