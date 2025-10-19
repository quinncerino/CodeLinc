#!/bin/bash
# AWS EC2 Deployment Script for BenefitLink

echo "🚀 BenefitLink AWS Deployment"
echo "=============================="

# Update system
sudo yum update -y

# Install Python 3
sudo yum install python3 python3-pip -y

# Install dependencies
pip3 install -r requirements.txt

# Configure AWS credentials (use IAM role instead for production)
# aws configure

# Create systemd service
sudo tee /etc/systemd/system/benefitlink.service > /dev/null <<EOF
[Unit]
Description=BenefitLink Streamlit App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/CodeLinc
ExecStart=/usr/local/bin/streamlit run enhanced_ui.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl enable benefitlink
sudo systemctl start benefitlink

echo "✅ Deployment complete!"
echo "Access at: http://YOUR_EC2_IP:8501"