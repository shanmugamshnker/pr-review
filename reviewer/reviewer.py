import os
import subprocess
from llm_client import hybrid_review
from github_client import post_inline_comment

def get_files_to_review():
    raw_base = os.getenv("GITHUB_BASE_REF", "main")
    base = f"origin/{raw_base}" if not raw_base.startswith("origin/") else raw_base

    try:
        result = subprocess.run(
            f"git diff --name-status {base} HEAD",
            shell=True, capture_output=True, text=True, check=True
        )
        file_status_lines = result.stdout.strip().splitlines()
        review_targets = {}

        for line in file_status_lines:
            parts = line.strip().split(maxsplit=1)
            if len(parts) != 2:
                continue

            status, filename = parts
            if status not in {"A", "M"} or not filename.lower().endswith(".py"):
                continue

            if status == "A":
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        review_targets[filename] = {"lines": f.readlines()}
                except Exception as e:
                    print(f"❌ Failed to read new file {filename}: {e}")

            elif status == "M":
                try:
                    diff_result = subprocess.run(
                        f"git diff --unified=5 --no-prefix {base} HEAD -- {filename}",
                        shell=True, capture_output=True, text=True, check=True
                    )
                    diff_lines = [
                        line[1:] for line in diff_result.stdout.splitlines()
                        if line.startswith("+") and not line.startswith("+++")
                    ]
                    if diff_lines:
                        review_targets[filename] = {"lines": diff_lines}
                except Exception as e:
                    print(f"❌ Failed to get diff for {filename}: {e}")

        return review_targets

    except subprocess.CalledProcessError as e:
        print("❌ Failed to get git diff:", e.stderr)
        return {}

def main():
    print("🚀 Starting AI Code Reviewer...")
    changed_files = get_files_to_review()
    if not changed_files:
        print("ℹ️ No relevant file changes found.")
        return

    print(f"📁 {len(changed_files)} file(s) to review.")

    for file_path, data in changed_files.items():
        try:
            code = "\n".join(data["lines"])
            print(f"🔍 Reviewing file: {file_path}...")

            comments = hybrid_review(code, file_path, runtime="python")

            for comment in comments:
                try:
                    post_inline_comment(
                        file_path=file_path,
                        line=comment["line"],
                        comment=comment["comment"],
                        suggestion=comment.get("suggestion")
                    )
                except Exception as e:
                    print(f"⚠️ Failed to post comment on {file_path}:{comment['line']}: {e}")

        except Exception as e:
            print(f"❌ Error reviewing {file_path}: {e}")

if __name__ == "__main__":
    main()
