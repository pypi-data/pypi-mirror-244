from typing import Dict, Any, Optional

import click
from click import Parameter, Context
from github import Github, Auth, Consts
from github.PullRequest import PullRequest
from github.PullRequestComment import PullRequestComment


class GithubClient:
    def __init__(self, access_token: str, url: str = Consts.DEFAULT_BASE_URL):
        auth = Auth.Token(access_token)
        self.github = Github(base_url=url, auth=auth)

    def find_pr(self, slug, original_branch: str, feature_branch: str) -> PullRequest | None:
        repo = self.github.get_repo(slug)
        pages = repo.get_pulls(base=original_branch, head=feature_branch)
        page = pages.get_page(0)
        if len(page) < 1:
            return None

        return page[0]

    def create_pr(self, slug: str, title: str, body: str, original_branch: str, feature_branch: str) -> PullRequest:
        repo = self.github.get_repo(slug)
        pr = self.find_pr(slug, original_branch, feature_branch)
        if pr is None:
            pr = repo.create_pull(title=title, body=body, base=original_branch, head=feature_branch)

        return pr

    def get_diff(self, slug, source_branch, target_branch):
        repo = self.github.get_repo(slug)
        repo.compare(source_branch, target_branch)

    def create_comment(self, pr: PullRequest, comment: Dict) -> PullRequestComment:
        return pr.create_review_comment(commit=pr.get_commits()[0], **comment)


class GithubClientClickType(click.ParamType):
    name = ""

    def convert(self, value: Any, param: Optional["Parameter"], ctx: Optional["Context"]) -> GithubClient:
        return GithubClient(access_token=value)
