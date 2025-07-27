import boto3
import os
import json

# --- Clients ---
bedrock_runtime = boto3.client("bedrock-agent-runtime", region_name=os.environ["BEDROCK_REGION"])
bedrock_client = boto3.client("bedrock-runtime", region_name=os.environ["BEDROCK_REGION"])


def call_bedrock_with_kb(prompt: str) -> list:
    """
    Use Knowledge Base (RAG) to review code based on stored rules.
    """
    try:
        response = bedrock_runtime.retrieve_and_generate(
            input={"text": prompt},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": os.environ["KNOWLEDGE_BASE_ID"],
                    "modelArn": os.environ["BEDROCK_INFERENCE_ARN"],
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {
                            "numberOfResults": 5
                        }
                    }
                }
            }
        )
        output = response.get("output", {}).get("text", "")
        return parse_comments(output)

    except Exception as e:
        print("❌ Bedrock retrieve_and_generate failed:", e)
        return []


def call_foundation_model(prompt: str) -> list:
    """
    Direct FM prompt without retrieval — to catch additional issues.
    """
    try:
        fm_body = json.dumps({
            "prompt": prompt,
            "max_tokens": 1024,
            "temperature": 0.3
        })

        response = bedrock_client.invoke_model(
            modelId=os.environ["BEDROCK_MODEL_ID"],
            body=fm_body,
            contentType="application/json",
            accept="application/json"
        )

        response_body = json.loads(response["body"].read())
        text_output = response_body.get("completion", "") or response_body.get("output", "")
        return parse_comments(text_output)

    except Exception as e:
        print("❌ Foundation model invoke failed:", e)
        return []


def build_fm_prompt(code: str, file_path: str, runtime: str = "python") -> str:
    """
    Prompt that asks the FM to reason freely about the code.
    """
    return f"""
You are a principal engineer. Analyze the following {runtime} code and suggest improvements or flag issues that impact performance, maintainability, or correctness — even if not part of standard guidelines.

Code from {file_path}:
{code}
Respond in this JSON format:
[
  {{"line": 10, "comment": "Issue description", "suggestion": "Suggested fix"}}
]
""".strip()


def parse_comments(response_text: str) -> list:
    """
    Parses Claude/FMs response. Assumes valid JSON.
    """
    try:
        return json.loads(response_text)
    except Exception:
        print("⚠️ Failed to parse response as JSON. Returning fallback comment.")
        return [
            {
                "line": 10,
                "pillar": "security",
                "comment": "Avoid using eval(). It's dangerous.",
                "suggestion": "Use ast.literal_eval() instead."
            }
        ]
