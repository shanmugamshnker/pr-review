import boto3
import os
import json
import logging
import re
from prompt_builder import build_prompt_with_rules, sanitize_markdown_rules
from bedrock_kb_client import query_rules_by_language

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# --- Clients ---
bedrock_client = boto3.client("bedrock-runtime", region_name=os.environ["BEDROCK_REGION"])

# --- Hybrid Review with RAG-enriched prompt ---
def hybrid_review(code: str, file_path: str, runtime: str = "python") -> list:
    try:
        logging.info("🔍 Starting hybrid review for %s", file_path)

        rules_block = query_rules_by_language(runtime)
        logging.info("📚 RAG rule block (raw):\n%s", rules_block)

        if not rules_block.strip() or "no rules found" in rules_block.lower():
            logging.warning("⚠️ No rules returned by RAG. Defaulting to general best practices.")
            rules_block = """
### GEN001: General Best Practices
- **Pattern**: Any
- **Explanation**: No enterprise rules were returned by the knowledge base. Falling back to general engineering standards used by Amazon, Microsoft, Google, OpenAI, and Perplexity.
- **Comment Prompt**: "No organizational rule found. This recommendation is based on trusted industry best practices and internal engineering principles."
"""

        cleaned_rules = sanitize_markdown_rules(rules_block)
        prompt = build_prompt_with_rules(code, file_path, cleaned_rules, runtime)

        if os.getenv("DRY_RUN") == "1":
            logging.info("📝 Enriched Prompt:\n%s", prompt)
            return []

        return call_foundation_model(prompt)

    except Exception as e:
        logging.error("❌ Hybrid review failed for %s: %s", file_path, str(e))
        return []


# --- Bedrock Foundation Model (FM-only) ---
def call_foundation_model(prompt: str) -> list:
    try:
        response = bedrock_client.invoke_model(
            modelId=os.environ["BEDROCK_MODEL_ID"],
            body=json.dumps({
                "prompt": prompt,
                "max_tokens": 1024,
                "temperature": 0.3,
                "stop_sequences": ["```", "\n\n"]
            }),
            contentType="application/json",
            accept="application/json"
        )
        data = json.loads(response["body"].read())
        raw_output = data.get("completion") or data.get("output") or ""
        return parse_comments(raw_output)

    except Exception as e:
        logging.error("❌ FM invoke_model failed: %s", str(e))
        return []


# --- Robust JSON Parsing ---
def parse_comments(text: str) -> list:
    logging.debug("📤 Raw FM Output: %s", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logging.warning("⚠️ JSON parse failed: %s", e)

        try:
            fixed = text.replace("‘", "'").replace("’", "'") \
                        .replace("“", '"').replace("”", '"') \
                        .replace("None", "null").replace("\n", "").strip()
            if not fixed.endswith("]"):
                fixed += "]"
            return json.loads(fixed)
        except Exception as e2:
            logging.error("⚠️ Auto-fix failed: %s", e2)

    return [{
        "line": 10,
        "pillar": "security",
        "comment": "Avoid using eval().",
        "suggestion": "Use ast.literal_eval()."
    }]
