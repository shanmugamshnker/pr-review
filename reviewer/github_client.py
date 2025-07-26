import os
from github import Github
from github.GithubException import GithubException

# Read env vars
token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")
pr_number = int(os.getenv("GITHUB_PR_NUMBER"))

# Init GitHub client
gh = Github(token)
repo = gh.get_repo(repo_name)
pr = repo.get_pull(pr_number)

def post_inline_comment(file_path, line, comment, suggestion=None):
    try:
        comment_body = f"🧠 **AI Review Suggestion**\n\n💬 {comment}"
        if suggestion:
            comment_body += f"\n\n💡 Suggestion:\n```python\n{suggestion}\n```"

        # Attempt inline comment using PR diff
        review_comments = [{
            "path": file_path,
            "body": comment_body,
            "line": line,
            "side": "RIGHT"
        }]
        pr.create_review(body="🤖 AI Code Review", event="COMMENT", comments=review_comments)
        print(f"✅ Inline comment posted on {file_path}:{line}")
    except GithubException as e:
        print(f"⚠️ Failed to post inline comment: {e.data if hasattr(e, 'data') else e}")
        fallback_comment = (
            f"🛠️ Could not add inline comment for `{file_path}` line {line}.\n"
            f"Here's the feedback instead:\n\n💬 {comment}"
        )
        if suggestion:
            fallback_comment += f"\n\n💡 Suggestion:\n```python\n{suggestion}\n```"
        try:
            pr.create_issue_comment(fallback_comment)
            print(f"📌 Fallback comment posted to PR.")
        except Exception as e2:
            print(f"❌ Failed to post fallback PR comment: {e2}")
