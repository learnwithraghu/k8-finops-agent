import boto3
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_with_bedrock(data, config):
    logger.info("Sending data to Bedrock...")
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    prompt = f"""You are a FinOps assistant. Analyze the following Kubernetes pod resource usage data.
Identify any pods that are over-provisioned or under-utilized.
Return a JSON array of findings with fields: pod_name, namespace, issue, recommendation.

Data:
{data}"""
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = client.invoke_model(
        modelId=config.get("model_id", "anthropic.claude-3-sonnet-20240229-v1:0"),
        body=json.dumps(body)
    )
    response_body = json.loads(response["body"].read())
    content = response_body["content"][0]["text"]
    logger.info("Received response from Bedrock")
    return content
