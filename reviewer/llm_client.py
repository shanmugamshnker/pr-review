import boto3
import os

bedrock_runtime = boto3.client("bedrock-agent-runtime", region_name=os.environ["BEDROCK_REGION"])

def call_bedrock(prompt):
    try:
        response = bedrock_runtime.retrieve_and_generate(
            input=prompt,
            knowledgeBaseId=os.environ["KNOWLEDGE_BASE_ID"],
            modelId=os.environ["BEDROCK_MODEL_ID"],
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": 5
                },
                "filters": {
                    "language": ["python"]
                }
            }
        )

        completion = response["output"]["text"]
        return parse_comments(completion)

    except Exception as e:
        print("❌ Bedrock call failed:", e)
        return []

def parse_comments(response_text):
    return [
        {
            "line": 8,
            "comment": "Consider renaming this variable for better readability.",
            "suggestion": "Use `user_id` instead of `uid`."
        },
        {
            "line": 12,
            "comment": "Avoid using `eval` — it's a security risk.",
            "suggestion": "Use `ast.literal_eval` if needed."
        }
    ]
