import os
from github import Github

def post_inline_comment(file_path: str, line: int, comment: str, suggestion: str = None):
    token = os.getenv("PAT")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number = int(os.getenv("GITHUB_PR_NUMBER"))

    gh = Github(token)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    commit_id = pr.head.sha

    full_comment = f"❌ {comment}"
    if suggestion:
        full_comment += f"\n💡 Suggestion: {suggestion}"

    pr.create_review_comment(
        body=full_comment,
        commit_id=commit_id,
        path=file_path,
        line=line,
        side="RIGHT"
    )
