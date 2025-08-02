# import boto3
# import os

# def query_rules_by_language(language: str) -> str:
#     client = boto3.client("bedrock-agent-runtime", region_name=os.getenv("BEDROCK_REGION"))

#     try:
#         response = client.retrieve(
#             knowledgeBaseId=os.getenv("KNOWLEDGE_BASE_ID"),
#             retrievalQuery={"text": f"{language} code review rules"},
#             retrievalConfiguration={
#                 "vectorSearchConfiguration": {
#                     "numberOfResults": 1
#                 }
#             }
#         )

#         results = response.get("retrievalResults", [])
#         return results[0]["content"]["text"] if results else "No rules found."

#     except Exception as e:
#         print(f"❌ Bedrock KB retrieve failed for {language}: {e}")
#         return ""


import os
import json
import logging
import boto3
from botocore.exceptions import ClientError

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Bedrock Agent Runtime Client
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')

# Environment variables
KB_ID = os.environ.get('BEDROCK_KB_ID')  # e.g., 'your-kb-id'
MODEL_ARN = os.environ.get('BEDROCK_MODEL_ARN')  # e.g., 'arn:aws:bedrock:...'

def lambda_handler(event, context):
    query = event.get("query") or "What is AWS Graviton?"
    
    if not KB_ID or not MODEL_ARN:
        logger.error("Missing KB_ID or MODEL_ARN in environment.")
        return {
            "statusCode": 500,
            "body": "Configuration error: Missing Knowledge Base ID or Model ARN."
        }

    try:
        logger.info(f"Sending query to Bedrock KB: {query}")
        response = bedrock_agent_runtime.retrieve_and_generate(
            input={
                "text": query
            },
            retrieveAndGenerateConfiguration={
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KB_ID
                },
                "modelArn": MODEL_ARN
            }
        )

        output_text = response.get("output", {}).get("text", "")
        citations = response.get("citations", [])
        return {
            "statusCode": 200,
            "body": json.dumps({
                "response": output_text,
                "citations": citations
            })
        }

    except ClientError as e:
        logger.error(f"AWS client error: {e}")
        return {
            "statusCode": 500,
            "body": f"AWS error: {e.response['Error']['Message']}"
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            "statusCode": 500,
            "body": f"Unhandled error: {str(e)}"
        }
