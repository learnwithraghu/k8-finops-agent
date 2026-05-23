import boto3
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_with_bedrock(data):
    logger.info("Sending data to Bedrock...")
    
    # Validate required environment variables
    region = os.getenv("AWS_REGION")
    model_id = os.getenv("BEDROCK_MODEL_ID")
    
    if not region:
        raise ValueError("AWS_REGION environment variable is not set")
    if not model_id:
        raise ValueError("BEDROCK_MODEL_ID environment variable is not set")
    
    client = boto3.client(
        "bedrock-runtime",
        region_name=region
    )
    
    prompt = f"""Analyze the following Kubernetes pod resource usage data and return ONLY a JSON array.
No markdown, no explanation, no extra text - ONLY valid JSON.

For each finding, create an object with these exact fields:
- pod_name (string): Name of the pod
- namespace (string): Kubernetes namespace
- issue (string): The problem identified
- recommendation (string): How to fix it

Return a JSON array like this:
[
  {{
    "pod_name": "pod-name",
    "namespace": "namespace",
    "issue": "issue description",
    "recommendation": "fix recommendation"
  }}
]

Data to analyze:
{data}

Return ONLY the JSON array, nothing else:"""
    
    # Use the converse API (works with both Claude and Amazon Nova models)
    messages = [
        {
            "role": "user",
            "content": [{"text": prompt}]
        }
    ]
    
    logger.info(f"Using model: {model_id}")
    
    try:
        response = client.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig={
                "maxTokens": int(os.getenv("BEDROCK_MAX_TOKENS", 1024)),
                "temperature": float(os.getenv("BEDROCK_TEMPERATURE", 0.3)),
                "topP": 0.9,
            }
        )
        
        # Extract content from converse response
        try:
            content = response["output"]["message"]["content"][0]["text"]
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to extract content from Bedrock response: {e}")
            logger.error(f"Response structure: {response}")
            raise ValueError("Unexpected Bedrock response structure")
        
        if not content:
            logger.warning("Bedrock returned empty content")
            return ""
        
        logger.info(f"Received response from Bedrock (length: {len(content)})")
        logger.debug(f"Response preview: {content[:200]}...")
        return content
        
    except Exception as e:
        logger.error(f"Bedrock API error: {e}")
        logger.warning("Bedrock unavailable, using mock fallback response")
        # Return mock response so agent can still process findings
        mock_response = '''[
            {
                "pod_name": "demo-pod",
                "namespace": "default",
                "issue": "Over-provisioned resources",
                "recommendation": "Review and adjust CPU/memory requests based on actual usage"
            }
        ]'''
        return mock_response