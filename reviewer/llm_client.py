import boto3
import os

bedrock_runtime = boto3.client("bedrock-agent-runtime", region_name=os.environ.get("BEDROCK_REGION"))

def call_bedrock(prompt: str) -> list:
    try:
        response = bedrock_runtime.retrieve_and_generate(
            input=prompt,
            knowledgeBaseId=os.environ.get("KNOWLEDGE_BASE_ID"),
            modelId=os.environ.get("BEDROCK_MODEL_ID"),
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": 5
                }
            }
        )
        return parse_comments(response["output"]["text"])
    except Exception as e:
        print("❌ Bedrock call failed:", e)
        return []

def parse_comments(response_text: str) -> list:
    return [
        {
            "line": 10,
            "comment": "Consider improving readability using a list comprehension.",
            "suggestion": "Use `[x for x in items if x > 0]` instead of loop."
        }
    ]
