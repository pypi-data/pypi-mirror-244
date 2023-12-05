import configparser
import os
import pathlib
from pathlib import Path
from typing import List, Optional, Any

import click
import requests
from click import Parameter, Context
from click.core import ParameterSource
from requests import RequestException
from git.repo.base import Repo

from patched_cli.models.common import Patch, VulnFile, CreatePullRequest

_OPEN_COUNT = 0
_HOME_FOLDER = Path(click.get_app_dir("Patched", force_posix=True))
_CONFIG_NAME = "config.ini"
_LOG_NAME = "patched.log"
LOG_FILE = _HOME_FOLDER / _LOG_NAME
CONFIG_FILE = _HOME_FOLDER / _CONFIG_NAME
TOKEN_URL = "https://app.patched.codes/signin"


def trigger_browser() -> None:
    global _OPEN_COUNT
    if _OPEN_COUNT < 1:
        _OPEN_COUNT = _OPEN_COUNT + 1
        click.launch(TOKEN_URL)


class PatchedClient(click.ParamType):
    def __init__(self, url: str, access_token: str):
        self.url = url
        self.access_token = access_token

    def test_token(self) -> bool:
        try:
            response = requests.post(self.url + "/token/test", headers={"Authorization": f"Bearer {self.access_token}"},
                                     json={})
        except requests.exceptions.ConnectionError:
            click.echo("Unable to establish connection to patched server")
            return False
        except RequestException as e:
            return False

        return response.ok and response.json()["msg"] == "ok"

    def get_patches(self, path: pathlib.Path, repo: Repo | None, vuln_files: List[VulnFile]) -> List[Patch]:
        branch_name = None
        original_remote_url = path.absolute().as_uri()
        if repo is not None:
            branch = repo.active_branch
            branch_name = branch.name
            tracking_branch = branch.tracking_branch()
            if tracking_branch is not None:
                original_remote_name = tracking_branch.remote_name
                original_remote_url = repo.remotes[original_remote_name].url

        response = requests.post(self.url + f"/patch",
                                 headers={"Authorization": f"Bearer {self.access_token}"},
                                 json={
                                     "url": original_remote_url,
                                     "branch": branch_name,
                                     "vuln_files": [vuln_file.model_dump() for vuln_file in vuln_files]
                                 })
        return [Patch(**patch) for patch in response.json()]

    def create_pr(self, repo_slug: str, path: str, diff_text: str, original_branch: str, next_branch: str,
                  patches: List[Patch]) -> str:
        create_pull_request = CreatePullRequest(repo_slug=repo_slug,
                                                path=path,
                                                diff_text=diff_text,
                                                original_branch_name=original_branch,
                                                next_branch_name=next_branch,
                                                applied_patches=patches)
        response = requests.post(self.url + "/create_pr", headers={"Authorization": f"Bearer {self.access_token}"},
                                 json=create_pull_request.model_dump())
        return response.json()["url"]


class _NotSet:
    """
    Mainly used to indicate None without using NoneType just so that the prompt is handled on our end,
    rather than on click.
    """

    def __init__(self):
        pass


class PatchedClientClickType(click.ParamType):
    name = ""

    def convert(self, value: Any, param: Optional["Parameter"], ctx: Optional["Context"]) -> PatchedClient:
        if ctx is None or param is None or param.name is None:
            raise ValueError("Unhandled usage of type")

        url = os.environ.get("PATCHED_URL", "https://patch-function-ps63srnnsq-de.a.run.app")
        source = ctx.get_parameter_source(param.name)

        # value can be either str, PatchedClient or _NotSet
        client = None
        if isinstance(value, str):
            client = PatchedClient(url, value)
        elif isinstance(value, PatchedClient):
            client = value

        if client is not None and client.test_token():
            return client

        if client is None:
            current_value = click.prompt(f"Opening login at: \"{TOKEN_URL}\".\n"
                                         "Please go to the Integration's tab and generate an API key.\n"
                                         "Please copy the access token that is generated, "
                                         "paste it into the terminal and press the return key.\n"
                                         "Token", hide_input=True)
            client = PatchedClient(url, current_value)
            if client.test_token():
                return client

            for _ in range(2):
                current_value = click.prompt("Invalid access token. Please try again.\n"
                                             "Access Token", hide_input=True)
                client = PatchedClient(url, current_value)
                if client.test_token():
                    return client
            click.echo("Access Token rejected too many times. Please verify that access token is correct.")
            ctx.abort()

        if source == ParameterSource.DEFAULT:
            click.echo(f"Access Token rejected from file \"{CONFIG_FILE}\".\n"
                       f"Please verify that the access token is correct or delete the file.")
            ctx.abort()

        if source == ParameterSource.ENVIRONMENT:
            click.echo(f"\n"
                       f"Access Token rejected from \"{param.envvar}\" environment variable.\n"
                       f"Please verify that the access token is correct.")
            ctx.abort()

        self.fail(f"Access Token rejected. Please verify that the access token is correct.")

    @staticmethod
    def default() -> str | _NotSet:
        _HOME_FOLDER.mkdir(exist_ok=True)

        if not CONFIG_FILE.exists():
            trigger_browser()
            return _NotSet()

        parser = configparser.ConfigParser()
        parser.read(CONFIG_FILE)
        if "patched" not in parser:
            trigger_browser()
            return _NotSet()

        if "access.token" not in parser["patched"]:
            trigger_browser()
            return _NotSet()

        return parser["patched"]["access.token"]

    @staticmethod
    def callback(ctx, param, value: PatchedClient) -> PatchedClient:
        _HOME_FOLDER.mkdir(exist_ok=True)
        CONFIG_FILE.touch(exist_ok=True)

        parser = configparser.ConfigParser()
        parser.read(CONFIG_FILE)

        is_changed = False
        if "patched" not in parser:
            parser.add_section("patched")
            is_changed = True
        if "access.token" not in parser["patched"]:
            parser["patched"] = {"access.token": value.access_token}
            is_changed = True

        if is_changed:
            with open(CONFIG_FILE, "w") as fp:
                parser.write(fp)

        return value
