# Deployment Guide

## Option 1: Streamlit Cloud (Easiest)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repo
4. Select `enhanced_ui.py` as main file
5. Add secrets in Streamlit dashboard:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION=us-east-2

## Option 2: AWS EC2

1. Launch EC2 instance
2. Install dependencies:
```bash
sudo yum install python3-pip
pip3 install -r requirements.txt
```

3. Configure AWS credentials
4. Run Streamlit:
```bash
streamlit run enhanced_ui.py --server.port 8501
```

## Option 3: HTML/React App (Requires Backend)

1. Deploy Flask API to AWS Lambda or EC2
2. Update API endpoint in app.html
3. Host app.html on S3 + CloudFront

## Recommended: Use Streamlit Cloud

It's free, handles AWS credentials securely, and deploys in minutes.