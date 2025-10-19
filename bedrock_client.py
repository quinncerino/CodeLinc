import boto3
import json

def get_financial_advice(question):
    try:
        client = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        # Try Amazon Nova first (should be available without approval)
        body = json.dumps({
            "messages": [{
                "role": "user",
                "content": [{
                    "text": f"You are a benefits advisor. {question}"
                }]
            }],
            "inferenceConfig": {
                "max_new_tokens": 1000,
                "temperature": 0.7
            }
        })
        
        response = client.invoke_model(
            modelId='amazon.nova-micro-v1:0',
            body=body
        )
        
        result = json.loads(response['body'].read())
        return result['output']['message']['content'][0]['text']
        
    except Exception as e:
        # For first-time Anthropic users, you may need to go to:
        # AWS Console → Bedrock → Model catalog → Claude 3 Haiku → Use case details
        print(f"Bedrock error: {e}")
        return f"""Based on your profile, here are my recommendations:

**Health Insurance**: Consider a mid-tier plan that balances cost and coverage.

**Dental & Vision**: Basic coverage recommended for preventive care.

**Employee Assistance Program**: Valuable for work-life balance support.

*Note: Demo response. For Anthropic models, first-time users may need to submit use case details in AWS Console → Bedrock → Model catalog.*"""

if __name__ == "__main__":
    advice = get_financial_advice("What health insurance options are available?")
    print("Answer:", advice)