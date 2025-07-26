import boto3
import os

bedrock_runtime = boto3.client("bedrock-agent-runtime", region_name=os.environ["BEDROCK_REGION"])

def call_bedrock(prompt: str) -> list:
    try:
        response = bedrock_runtime.retrieve_and_generate(
            input=prompt,
            knowledgeBaseId=os.environ["KNOWLEDGE_BASE_ID"],
            modelId=os.environ["BEDROCK_MODEL_ID"],
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": 5
                }
            },
            filters={  # ✅ Correctly placed
                "andAll": [
                    {"equals": {"key": "language", "value": "python"}}
                ]
            }
        )
        completion = response["output"]["text"]
        return parse_comments(completion)

    except Exception as e:
        print("❌ Bedrock retrieve_and_generate failed:", e)
        return []

def parse_comments(response_text: str) -> list:
    return [
        {
            "line": 10,
            "comment": "Improve loop logic.",
            "suggestion": "Use a comprehension instead."
        }
    ]
