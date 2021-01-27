#!/bin/bash

# Description: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html


pip install --target ./package requests






zip litquidity-chatbot.zip lambda_function.py \
    ./main/__init__.py \
    ./main/balancesheetgetter/BalanceSheetGetter.py \
    ./main/balancesheetgetter/__init__.py \
    ./main/datastructures/AnalysisMethod.py \
    ./main/datastructures/CustomerMetrics.py \
    ./main/datastructures/StockFinancialMetadata.py \
    ./main/datastructures/StockInfoContainer.py \
    ./main/datastructures/StockScore.py \
    ./main/datastructures/__init__.py \
    ./main/portfoliobuilder/PortfolioBuilder.py \
    ./main/portfoliobuilder/__init__.py \
    ./main/priceanalysis/PriceForecaster.py \
    ./main/priceanalysis/__init__.py \
    ./main/pricegetter/PriceGetter.py \
    ./main/pricegetter/__init__.py \
    ./main/stockfilter/StockFilter.py \
    ./main/stockfilter/__init__.py \
    ./main/valuation/ValuationCalculator.py \
    ./main/valuation/__init__.py

aws lambda update-function-code --function-name project2_get_recommended_portfolio --zip-file fileb://litquidity-chatbot.zip
