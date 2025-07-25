import boto3
import json
import os

def call_bedrock(prompt: str):
    client = boto3.client("bedrock-runtime", region_name=os.getenv("BEDROCK_REGION"))
    response = client.invoke_model(
        modelId=os.getenv("BEDROCK_MODEL_ID"),
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "prompt": prompt,
            "max_tokens": 1024,
            "temperature": 0.3
        })
    )
    output = json.loads(response["body"].read())
    try:
        return json.loads(output["completion"])
    except:
        return []
