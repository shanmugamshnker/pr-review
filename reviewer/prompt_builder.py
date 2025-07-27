from bedrock_kb_client import query_rules_by_pillar

def build_prompt(code: str, file_path: str, runtime: str = "python") -> str:
    pillars = ["security", "style", "readability", "best_practices"]
    prompt = f"You are a Principal Engineer and expert reviewer for {runtime} code.\n"
    prompt += "Your responsibility is to enforce code quality across the following 4 pillars:\n"
    prompt += "- 🔐 Security\n- 🎨 Code Style\n- 👁️ Readability\n- 🧠 Best Practices\n"
    prompt += "Use the following rules to guide your review:\n"

    for pillar in pillars:
        rules = query_rules_by_pillar(runtime, pillar)
        prompt += f"\n[{pillar.upper()} RULES]\n{rules}\n"

    prompt += f"\nCode to review from {file_path}:\n```\n{code}\n```\n"
    prompt += "Respond ONLY in this JSON format:\n"
    prompt += '[{"line": 10, "pillar": "security", "comment": "Avoid eval.", "suggestion": "Use ast.literal_eval() instead."}]'

    return prompt
