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
source venv/bin/activate

# Download dependencies to local directory - Targeted directory
pip install --target ./package requests
pip install --target ./package python-dotenv
pip install --target ./package alpaca-trade-api
pip install --target ./package pandas

# Install dependencies - Virtual Environment
#pip install python-dotenv
#pip install alpaca-trade-api
#pip install requests
#pip install pandas
##pip install scikit-learn
##pip install imbalanced-learn
##pip install pydotplus
##pip install spacy
##pip install python -m spacy download en_core_web_sm
##pip install imblearn
##pip install psycopg2
##pip install arch
##pip install intake
##pip install intake-parquet
##pip install wordcloud
##pip install tabulate
##pip install asyncio
##pip install iexfinance
##pip install tesseract
##pip install chatterbot
##pip install --upgrade tensorflow
##npm install dotenv
##pip install newsapi-python==0.2.5





zip litquidity-chatbot.zip -r lambda_function.py main/ package/

#zip litquidity-chatbot.zip lambda_function.py \
#    ./main/__init__.py \
#    ./main/balancesheetgetter/BalanceSheetGetter.py \
#    ./main/balancesheetgetter/__init__.py \
#    ./main/datastructures/AnalysisMethod.py \
#    ./main/datastructures/CustomerMetrics.py \
#    ./main/datastructures/StockFinancialMetadata.py \
#    ./main/datastructures/StockInfoContainer.py \
#    ./main/datastructures/StockScore.py \
#    ./main/datastructures/__init__.py \
#    ./main/portfoliobuilder/PortfolioBuilder.py \
#    ./main/portfoliobuilder/__init__.py \
#    ./main/priceanalysis/PriceForecaster.py \
#    ./main/priceanalysis/__init__.py \
#    ./main/pricegetter/PriceGetter.py \
#    ./main/pricegetter/__init__.py \
#    ./main/stockfilter/StockFilter.py \
#    ./main/stockfilter/__init__.py \
#    ./main/valuation/ValuationCalculator.py \
#    ./main/valuation/__init__.py \
#    package

aws lambda update-function-code --function-name project2_get_recommended_portfolio --zip-file fileb://litquidity-chatbot.zip
