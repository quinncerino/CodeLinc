# AWS Configuration Guide

## Step 1: Install AWS CLI
```bash
# macOS
brew install awscli

# Windows
# Download from: https://aws.amazon.com/cli/

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

## Step 2: Create AWS Account & Get Credentials
1. Go to https://aws.amazon.com → Create Account
2. Go to IAM Console → Users → Create User
3. Attach policies: `AmazonBedrockFullAccess`, `AmazonDynamoDBFullAccess`
4. Create Access Key → Download credentials

## Step 3: Configure AWS CLI
```bash
aws configure
# Enter:
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region: us-east-1
# Default output format: json
```

## Step 4: Enable Bedrock Models
1. Go to AWS Console → Bedrock → Model access
2. Click "Request model access"
3. Select "Claude 3 Haiku" → Submit
4. Wait for approval (usually instant)

## Step 5: Create DynamoDB Table
```bash
python create_dynamodb_table.py
```

## Step 6: Test Configuration
```bash
python bedrock_client.py
```

## Environment Variables (Alternative)
```bash
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
export AWS_DEFAULT_REGION="us-east-1"
```