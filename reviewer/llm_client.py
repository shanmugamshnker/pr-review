import boto3
import os

# Initialize Bedrock Agent Runtime client
bedrock_runtime = boto3.client("bedrock-agent-runtime", region_name=os.environ["BEDROCK_REGION"])

def call_bedrock(prompt: str) -> list:
    try:
        response = bedrock_runtime.retrieve_and_generate(
            input={"text": prompt},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": os.environ["KNOWLEDGE_BASE_ID"],
                    "modelArn": os.environ["BEDROCK_MODEL_ID"],
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {
                            "numberOfResults": 5
                        }
                    }
                }
            }
        )

        completion = response["output"]["text"]
        return parse_comments(completion)

    except Exception as e:
        print("❌ Bedrock retrieve_and_generate failed:", e)
        return []

def parse_comments(response_text: str) -> list:
    # ⚠️ Update this parser as per real Claude output format.
    return [
        {
            "line": 10,
            "pillar": "security",
            "comment": "Avoid using eval(). It's dangerous.",
            "suggestion": "Use ast.literal_eval() instead."
        }
    ]
