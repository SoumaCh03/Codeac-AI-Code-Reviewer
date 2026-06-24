import logging
from typing import List, Dict, Any
from app.services.github.client import GitHubAppClient

logger = logging.getLogger(__name__)

class GitHubPRService:
    def __init__(self, installation_id: int):
        self.github = GitHubAppClient()
        self.client = self.github.get_client_for_installation(installation_id)

    def get_pr_diff(self, owner: str, repo: str, pull_number: int) -> str:
        """Fetches the raw diff of a Pull Request."""
        logger.info(f"Fetching diff for {owner}/{repo} PR #{pull_number}")
        headers = self.client.headers.copy()
        headers["Accept"] = "application/vnd.github.v3.diff"
        
        response = self.client.get(
            f"/repos/{owner}/{repo}/pulls/{pull_number}",
            headers=headers
        )
        response.raise_for_status()
        return response.text

    def post_review_comment(self, owner: str, repo: str, pull_number: int, commit_id: str, path: str, line: int, body: str):
        """Posts a review comment on a specific line of code."""
        payload = {
            "body": body,
            "commit_id": commit_id,
            "path": path,
            "line": line,
            "side": "RIGHT"
        }
        response = self.client.post(
            f"/repos/{owner}/{repo}/pulls/{pull_number}/comments",
            json=payload
        )
        if response.status_code not in (200, 201):
            logger.error(f"Failed to post comment: {response.text}")
        return response.json()

    def post_issue_comment(self, owner: str, repo: str, issue_number: int, body: str):
        """Posts a general comment on the PR (Issue)."""
        payload = {"body": body}
        response = self.client.post(
            f"/repos/{owner}/{repo}/issues/{issue_number}/comments",
            json=payload
        )
        if response.status_code not in (200, 201):
            logger.error(f"Failed to post issue comment: {response.text}")
        return response.json()
