#!/usr/bin/env python3
import boto3
import json

def test_aws_config():
    print("Testing AWS Configuration...")
    
    # Test credentials
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ AWS Credentials: {identity['Arn']}")
    except Exception as e:
        print(f"❌ AWS Credentials: {e}")
        return False
    
    # Test DynamoDB
    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('UserBenefitsContext')
        table.load()
        print("✅ DynamoDB: Table exists")
    except Exception as e:
        print(f"❌ DynamoDB: {e}")
    
    # Test Bedrock
    try:
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 10,
            "messages": [{"role": "user", "content": "Hi"}]
        })
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=body
        )
        print("✅ Bedrock: Model access enabled")
        return True
    except Exception as e:
        print(f"❌ Bedrock: {e}")
        return False

if __name__ == "__main__":
    test_aws_config()