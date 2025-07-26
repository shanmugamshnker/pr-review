import boto3
import os

def query_rules_by_pillar(language: str, pillar: str) -> str:
    client = boto3.client("bedrock-agent-runtime", region_name=os.getenv("BEDROCK_REGION"))

    try:
        response = client.retrieve(
            knowledgeBaseId=os.getenv("KNOWLEDGE_BASE_ID"),
            retrievalQuery={"text": f"{language} {pillar} code review rules"},
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": 1,
                    "filter": {
                        "andAll": [
                            {"equals": {"key": "language", "value": "python"}},
                            {"equals": {"key": "pillar", "value": "security"}}
                        ]
                    }
                }
            }
        )

        results = response.get("retrievalResults", [])
        return results[0]["content"]["text"] if results else "No rules found."

    except Exception as e:
        print(f"❌ Bedrock KB retrieve failed: {e}")
        return ""
