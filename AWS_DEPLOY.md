# AWS Deployment Guide for BenefitLink

## Option 1: EC2 (Recommended)

### Step 1: Launch EC2 Instance
1. Go to AWS Console → EC2 → Launch Instance
2. Choose **Amazon Linux 2023**
3. Instance type: **t3.medium** (2 vCPU, 4GB RAM)
4. Create/select key pair
5. Security Group: Allow ports **22 (SSH)** and **8501 (Streamlit)**
6. Launch instance

### Step 2: Attach IAM Role
1. Create IAM role with policies:
   - `AmazonBedrockFullAccess`
   - `AmazonDynamoDBFullAccess`
2. Attach role to EC2 instance

### Step 3: Deploy Application
```bash
# SSH into EC2
ssh -i your-key.pem ec2-user@YOUR_EC2_IP

# Clone repository
git clone https://github.com/YOUR_USERNAME/CodeLinc.git
cd CodeLinc

# Run deployment script
chmod +x deploy_aws.sh
./deploy_aws.sh
```

### Step 4: Access Application
Open browser: `http://YOUR_EC2_IP:8501`

---

## Option 2: Streamlit Cloud (Easiest)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/CodeLinc.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `YOUR_USERNAME/CodeLinc`
5. Main file: `enhanced_ui.py`
6. Click "Deploy"

### Step 3: Add Secrets
In Streamlit Cloud dashboard → Settings → Secrets:
```toml
AWS_ACCESS_KEY_ID = "your_key"
AWS_SECRET_ACCESS_KEY = "your_secret"
AWS_DEFAULT_REGION = "us-east-2"
```

---

## Option 3: AWS Amplify

### Step 1: Create Dockerfile
Already created in repository

### Step 2: Deploy
1. Go to AWS Amplify Console
2. Connect GitHub repository
3. Build settings: Use Dockerfile
4. Deploy

---

## Recommended: Streamlit Cloud
- Free tier available
- Automatic HTTPS
- Easy updates via GitHub
- No server management