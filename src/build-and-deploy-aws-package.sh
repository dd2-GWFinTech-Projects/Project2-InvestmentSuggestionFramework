#!/bin/bash

# Description: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

# Initial configuration
## Install AWS CLI
#curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#unzip awscliv2.zip
#sudo ./aws/install

## Configure AWS CLI
#aws configure



# Make virtual environment
#virtualenv venv
#source venv/bin/activate

# Package the code
zip litquidity-chatbot.zip -r lambda_function.py main/
#zip litquidity-chatbot.zip -r lambda_function.py main/ .package/

# Download dependencies to local directory - Targeted directory
pip install --target ./.package requests
pip install --target ./.package python-dotenv
pip install --target ./.package alpaca-trade-api
pip install --target ./.package pandas
pip install --target ./.package statsmodels

# Add the dependencies to the package root
cd .package
zip -r ../litquidity-chatbot.zip .
cd ..

# Upload and deploy the function code to AWS Lambda
aws lambda update-function-code --function-name project2_get_recommended_portfolio --zip-file fileb://litquidity-chatbot.zip
