import os
from github import Github
from github.GithubException import GithubException

# --- 🔍 Sanitize and validate environment variables ---
token = os.getenv("PAT", "").strip()
repo_name = os.getenv("GITHUB_REPOSITORY", "").strip()
pr_number_str = os.getenv("GITHUB_PR_NUMBER", "").strip()

# Debug logs
print("🔧 Environment variables:")
print(f"  PAT Provided: {'✅' if token else '❌'}")
print(f"  Repository  : '{repo_name}'")
print(f"  PR Number   : '{pr_number_str}'")

if not token or not repo_name or not pr_number_str:
    raise RuntimeError("❌ Missing required environment variables: PAT, GITHUB_REPOSITORY, or GITHUB_PR_NUMBER")

try:
    pr_number = int(pr_number_str)
except ValueError:
    raise ValueError(f"❌ Invalid PR number: {pr_number_str}")

# --- 🛠️ GitHub Client Setup ---
gh = Github(token)

try:
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
except GithubException as e:
    print("❌ GitHub access failed.")
    print("🔎 Error:", e.data if hasattr(e, "data") else str(e))
    raise

# --- 🧠 Post Inline Comment Function ---
def post_inline_comment(file_path, line, comment, suggestion=None):
    try:
        comment_body = f"🧠 **AI Review Suggestion**\n\n💬 {comment}"
        if suggestion:
            comment_body += f"\n\n💡 Suggestion:\n```python\n{suggestion}\n```"

        # GitHub API expects line numbers relative to the diff (not always source file)
        review_comments = [{
            "path": file_path,
            "body": comment_body,
            "line": line,
            "side": "RIGHT"
        }]

        pr.create_review(
            body="🤖 AI Code Review Suggestions",
            event="COMMENT",
            comments=review_comments
        )

        print(f"✅ Inline comment posted on {file_path}:{line}")

    except GithubException as e:
        print(f"⚠️ Inline comment failed: {e.data if hasattr(e, 'data') else e}")
        fallback_comment = (
            f"🛠️ Could not post inline comment for `{file_path}` line {line}.\n"
            f"💬 {comment}"
        )
        if suggestion:
            fallback_comment += f"\n\n💡 Suggestion:\n```python\n{suggestion}\n```"

        try:
            pr.create_issue_comment(fallback_comment)
            print("📌 Fallback PR comment posted.")
        except Exception as e2:
            print(f"❌ Failed to post fallback comment: {e2}")
