import os
import subprocess
from prompt_builder import build_prompt
from llm_client import call_bedrock
from github_client import post_inline_comment

def get_changed_files_from_git():
    try:
        base = os.getenv("GITHUB_BASE_REF", "origin/main")
        head = "HEAD"

        print(f"🔍 Running diff: git diff {base} {head}")
        diff_cmd = f"git diff --unified=5 --no-prefix {base} {head}"
        result = subprocess.run(diff_cmd, shell=True, capture_output=True, text=True, check=True)

        if not result.stdout.strip():
            raise ValueError("Empty diff")

        return result.stdout

    except Exception as e:
        print(f"⚠️ Git diff failed: {e}")
        print("🔁 Falling back to full scan of all .py files")
        return get_all_python_files_as_diff()

def get_all_python_files_as_diff():
    """
    Fallback mechanism: Simulate a diff for all .py files.
    """
    simulated_diff = ""
    for root, _, files in os.walk("."):
        for fname in files:
            if fname.endswith(".py") and "reviewer.py" not in fname:
                path = os.path.join(root, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        simulated_diff += f"+++ {path}\n"
                        for line in lines:
                            simulated_diff += f"+{line}"
                except Exception as e:
                    print(f"❌ Failed to read {path}: {e}")
    return simulated_diff

def parse_unified_diff(diff_text):
    files = {}
    current_file = None
    for line in diff_text.splitlines():
        if line.startswith("+++ ") and not line.startswith("+++ /dev/null"):
            current_file = line.replace("+++ ", "").strip()
            files[current_file] = {"lines": []}
        elif current_file and (line.startswith("+") and not line.startswith("+++")):
            files[current_file]["lines"].append(line[1:])
    return files

def main():
    print("🚀 Starting AI Code Reviewer...")
    diff_text = get_changed_files_from_git()
    if not diff_text:
        print("ℹ️ No changes detected or error in git diff.")
        return

    changed_files = parse_unified_diff(diff_text)
    if not changed_files:
        print("ℹ️ No relevant file changes found.")
        return

    for file_path, data in changed_files.items():
        try:
            code = "\n".join(data["lines"])
            print(f"🔍 Reviewing file: {file_path}...")
            prompt = build_prompt(code, file_path, runtime="python")
            comments = call_bedrock(prompt)
            for comment in comments:
                try:
                    post_inline_comment(file_path, comment["line"], comment["comment"], comment.get("suggestion"))
                except Exception as e:
                    print(f"⚠️ Failed to post comment on {file_path}:{comment['line']}: {e}")
        except Exception as e:
            print(f"❌ Error reviewing {file_path}: {e}")

if __name__ == "__main__":
    main()
