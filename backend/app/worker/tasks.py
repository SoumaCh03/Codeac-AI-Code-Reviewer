import json
import logging
import os
import subprocess
import tempfile

from app.services.ai.agents import run_review_workflow
from app.services.github import GitHubPRService
from app.worker.celery_app import celery_app

logger = logging.getLogger(__name__)


def run_semgrep(diff_text: str) -> list:
    """Writes diff to a temp file and runs semgrep locally.
    In a real scenario, you'd checkout the actual files."""
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # We are writing the diff to a dummy python file just to see if semgrep catches anything.
            # Real enterprise SaaS would clone the repo shallowly at the head_sha.
            file_path = os.path.join(tmpdir, "changed_file.py")
            with open(file_path, "w") as f:
                f.write(diff_text)

            result = subprocess.run(
                ["semgrep", "scan", "--config", "auto", "--json", tmpdir],
                capture_output=True,
                text=True,
            )

            if result.stdout:
                parsed = json.loads(result.stdout)
                return parsed.get("results", [])
    except Exception as e:
        logger.error(f"Semgrep execution failed: {e}")
    return []


@celery_app.task(name="app.worker.tasks.process_pull_request")
def process_pull_request(payload: dict):
    logger.info("Processing PR webhook...")
    try:
        # Extract GitHub metadata
        installation_id = payload.get("installation", {}).get("id")
        pull_request = payload.get("pull_request", {})
        repo = payload.get("repository", {})

        if not installation_id or not pull_request or not repo:
            logger.warning("Missing required payload fields")
            return

        owner_name = repo.get("owner", {}).get("login")
        repo_name = repo.get("name")
        pr_number = pull_request.get("number")

        github_service = GitHubPRService(installation_id)

        # 1. Fetch Diff
        diff_text = github_service.get_pr_diff(owner_name, repo_name, pr_number)

        # 2. Run Static Analysis (Semgrep)
        semgrep_results = run_semgrep(diff_text)
        logger.info(f"Semgrep found {len(semgrep_results)} issues.")

        # 3. Run AI Workflow
        ai_results = run_review_workflow(diff_text)
        ai_findings = (
            ai_results.get("security_findings", [])
            + ai_results.get("performance_findings", [])
            + ai_results.get("architecture_findings", [])
        )

        # 4. Compile Report & Post Comments
        report_body = "### 🤖 Autonomous Code Review Results\n\n"

        if ai_findings:
            report_body += "#### AI Findings\n"
            for f in ai_findings:
                report_body += f"- **{f['severity'].upper()}**: {f['title']}\n  {f['description']}\n\n"

        if semgrep_results:
            report_body += "#### Static Analysis (Semgrep)\n"
            for r in semgrep_results:
                msg = r.get("extra", {}).get("message", "")
                report_body += (
                    f"- **{r.get('extra', {}).get('severity', 'WARNING')}**: {msg}\n"
                )

        if not ai_findings and not semgrep_results:
            report_body += "✅ No major issues found in this PR. Looks good to go!\n"

        github_service.post_issue_comment(owner_name, repo_name, pr_number, report_body)

        # In a real app, save to database here using SessionLocal()
        logger.info(f"Successfully processed PR #{pr_number}")
        return {
            "status": "success",
            "ai_findings": len(ai_findings),
            "semgrep_findings": len(semgrep_results),
        }

    except Exception as e:
        logger.exception(f"Error processing PR: {e}")
        return {"status": "error", "message": str(e)}
