# --------------------------------------------------------------------------
# Time Series Basics
# --------------------------------------------------------------------------

# Initial imports
import pandas as pd
import os
import datetime
import requests
import alpaca_trade_api as tradeapi
from pathlib import Path
from datetime import datetime,date
import hvplot.pandas
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np
import alpaca_trade_api as tradeapi
import ccxt

from dotenv import load_dotenv
from MCForecastTools import MCSimulation

class PriceForecaster:

    def __init__(self):

        # --------------------------------------------------------------------------
        # Load environment variables
        # --------------------------------------------------------------------------

        load_dotenv()

        # Import environment variables
        Kraken_Public_Key = os.getenv("KRAKEN_API_KEY")
        Kraken_Secret_Key = os.getenv("KRAKEN_SECRET_KEY")

    def run(self):

        # Set the public and private keys for the API
        exchange = ccxt.kraken({
            'apiKey': Kraken_Public_Key,
            'secret': Kraken_Secret_Key,
        })


        # Verify that environment variables were loaded
        # print(f"Kraken key data type: {type(Kraken_Public_Key)}")
        # print(f"Kraken secren data type: {type(Kraken_Secret_Key)}")

        # Connect to Kraken and load the available cryptocurrencies
        Crypto_Details = exchange.load_markets()

        # Import data as a Pandas DataFrame
        Crypto_df = pd.DataFrame(Crypto_Details)


        # ## Fetch Historical Data for BTC/USD and ETH/USD

        # Fetch daily candlestick bar data from `BTC/USD`
        BTC_Historical_Prices = exchange.fetch_ohlcv("BTC/USD", "1d")
        # Fetch daily candlestick bar data from `ETH/USD`
        ETH_Historical_Prices = exchange.fetch_ohlcv("ETH/USD", "1d")
        # Fetch daily candlestick bar data from `XRP/USD`
        XRP_Historical_Prices = exchange.fetch_ohlcv("XRP/USD", "1d")

        # Import the data as a Pandas DataFrame and set the columns
        BTC_Historical_Prices_df = pd.DataFrame(
            BTC_Historical_Prices, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        ETH_Historical_Prices_df = pd.DataFrame(
            ETH_Historical_Prices, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        XRP_Historical_Prices_df = pd.DataFrame(
            XRP_Historical_Prices, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )


        # Convert epoch timestamp to date using the `to_datetime` function and `unit` parameter
        BTC_Historical_Prices_df["date"] = pd.to_datetime(
            BTC_Historical_Prices_df["timestamp"], unit="ms"
        )
        ETH_Historical_Prices_df["date"] = pd.to_datetime(
            ETH_Historical_Prices_df["timestamp"], unit="ms"
        )
        XRP_Historical_Prices_df["date"] = pd.to_datetime(
            XRP_Historical_Prices_df["timestamp"], unit="ms"
        )


        # Pick all Cryptos close prices
        BTC_df = BTC_Historical_Prices_df.drop(columns=["timestamp", "open", "high", "low", "volume"])
        ETH_df = ETH_Historical_Prices_df.drop(columns=["timestamp", "open", "high", "low", "volume"])
        XRP_df = XRP_Historical_Prices_df.drop(columns=["timestamp", "open", "high", "low", "volume"])
        # Use the `rename` function and set the `columns` parameter to a dictionary of new column names
        BTC_df = BTC_df.rename(columns={
            "close": "BTC Close",
            "date": "Date"
        })
        ETH_df = ETH_df.rename(columns={
            "close": "ETH Close",
            "date": "Date 1"
        })
        XRP_df = XRP_df.rename(columns={
            "close": "XRP Close",
            "date": "Date 2"
        })


        # Use a list of re-ordered column names to alter the column order of the original DataFrame
        BTC_df = BTC_df[["Date", "BTC Close"]]
        ETH_df = ETH_df[["Date 1", "ETH Close"]]
        XRP_df = XRP_df[["Date 2", "XRP Close"]]

        # Concatenate all DataFrames into a single DataFrame
        Combined_Cryptos = pd.concat([ BTC_df, ETH_df, XRP_df ], axis="columns", join="inner")
        Combined_Cryptos.sort_index(inplace=True)


        # Remove extra date columns
        Combined_Cryptos = Combined_Cryptos.drop(columns=["Date 1", "Date 2"])


        # Select all rows for 1 Day
        Combined_price_1day = Combined_Cryptos.loc['2021-01-07':'2021-01-11']

        # --------------------------------------------------------------------------
        # Portfolio Analysis
        # --------------------------------------------------------------------------

        # Set Alpaca API key and secret
        Alpaca_API_Key = os.getenv("ALPACA_API_KEY")
        Alpaca_Secret_Key = os.getenv("ALPACA_SECRET_KEY")

        # Create the Alpaca API object
        Alpaca = tradeapi.REST(
            Alpaca_API_Key,
            Alpaca_Secret_Key,
            api_version="v2")

        # Format current date as ISO format
        #Start_Date = pd.to_datetime('2016-01-1', parse_dates=True)
        #End_Date = pd.to_datetime('2021-01-11', parse_dates=True)
        Start_Date = pd.Timestamp("2016-01-1").isoformat()
        End_Date = pd.Timestamp("2021-01-11").isoformat()

        # Set the tickers
        tickers = ["AAPL"]

        #"BXP", "PLD", "NOC", "BA", "PYPL", "SQ", "JNJ", "PFE", "TSLA",
        # Set timeframe to '1D' for Alpaca API
        timeframe = "1D"

        # Get current closing prices for all Stocks
        Data = Alpaca.get_barset(
            tickers,
            timeframe,
            start = Start_Date,
            end = End_Date
        ).df


        # Format the DateTime to remove Time
        Data.index = Data.index.strftime("%Y-%m-%d")


        # Pick all Stocks volumes
        AAPL_volume_df = Data["AAPL"]["volume"]


        # Rename Column
        AAPL_volume_df.columns = ["Apple"]


        # Select all rows for 5 Days
        volume_5days = AAPL_volume_df.loc['2021-01-05':'2021-01-11']


        # Select all rows for 1 Month
        volume_1Month = AAPL_volume_df.loc['2020-12-11':'2021-01-11']


        # Select all rows for 6 Months
        volume_6Months = AAPL_volume_df.loc['2020-06-11':'2021-01-11']


        # Select all rows for 1 Year
        volume_1Year = AAPL_volume_df.loc['2019-12-11':'2021-01-11']

        # Pick all Stocks close prices
        AAPL_close_df = Data["AAPL"]["close"]
        # Rename Column
        AAPL_close_df.columns = ["Apple"]

        # Select all rows for 5 Days
        price_5days = AAPL_close_df.loc['2021-01-05':'2021-01-11']
        # Select all rows for 1 Month
        price_1Month = AAPL_close_df.loc['2020-12-11':'2021-01-11']
        # Select all rows for 6 Months
        price_6Months = AAPL_close_df.loc['2020-06-11':'2021-01-11']
        # Select all rows for 1 Year
        price_1Year = AAPL_close_df.loc['2019-12-11':'2021-01-11']


        # Calculate Daily Returns for all the stocks
        BXP_df = BXP_df.pct_change()
        PLD_df = PLD_df.pct_change()
        NOC_df = NOC_df.pct_change()
        BA_df = BA_df.pct_change()
        PYPL_df = PYPL_df.pct_change()
        SQ_df = SQ_df.pct_change()
        JNJ_df = JNJ_df.pct_change()
        PFE_df = PFE_df.pct_change()
        TSLA_df = TSLA_df.pct_change()
        AAPL_df = AAPL_df.pct_change()
        SPY_df = SPY_df.pct_change()

        # --------------------------------------------------------------------------
        # ## Combining Daily Returns
        # --------------------------------------------------------------------------

        # Concatenate all DataFrames into a single DataFrame
        Combined_PCT_Returns = pd.concat([ BXP_df, PLD_df, NOC_df, BA_df, PYPL_df, SQ_df, JNJ_df, PFE_df, TSLA_df, AAPL_df, SPY_df ], axis="columns", join="inner")
        Combined_PCT_Returns.sort_index(inplace=True)


        # Count nulls
        Combined_PCT_Returns.isnull().sum()

        # Drop nulls
        Combined_PCT_Returns.dropna(inplace=True)


        # Rename Column
        Combined_PCT_Returns.columns = ["Boston Properties", "Prologis", "Northrop Grumman", "Boeing", "Paypal Holdings", "Square", "Johnson & Johnson", "Pfizer", "Tesla", "Apple", "S&P 500"]
        Combined_PCT_Returns.tail()

        # --------------------------------------------------------------------------
        # ## Daily Returns
        # --------------------------------------------------------------------------

        # Plot the closing prices using a line plot
        # Combined_PCT_Returns

        # --------------------------------------------------------------------------
        # ### Cumulative Returns
        # --------------------------------------------------------------------------

        # Plot cumulative returns??????????????
        Cumulative_Returns = (1 + Combined_PCT_Returns).cumprod()

        # --------------------------------------------------------------------------
        # ## Risk
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # ## Standard Deviation
        # --------------------------------------------------------------------------

        # Daily Standard Deviations for each portfolio.
        Combined_PCT_Returns_STD = pd.DataFrame(Combined_PCT_Returns.std())
        Combined_PCT_Returns_STD.columns = ["Daily Standard Deviation"]


        # Determine which portfolios are riskier than the S&P 500
        # print("The Below Portfolios are Riskier than S&P 500")
        Riskier_GSPC = Combined_PCT_Returns_STD.loc[Combined_PCT_Returns_STD["Daily Standard Deviation"] > Combined_PCT_Returns_STD.loc["S&P 500", "Daily Standard Deviation"]]

        # --------------------------------------------------------------------------
        # ## Exponentially Weighted Moving Average
        # --------------------------------------------------------------------------

        # Calculate a rolling window using the exponentially weighted moving average.
        Combined_PCT_Returns.ewm(halflife = 21).std()

        # --------------------------------------------------------------------------
        # ## Analysis
        # --------------------------------------------------------------------------

        # print("Our analysis includes the following:")
        # print("==========================================================================")
        # # The annualized standard deviation (252 trading days) for all portfolios:
        # print("The annualized standard deviation (252 trading days) for all portfolios:")
        # Annualized = Combined_PCT_Returns.rolling(window=252).std()
        # Annualized.dropna(inplace=True)
        # print(Annualized.tail())

        # The plotted rolling standard deviation using a 21 trading day window for all portfolios:
        # print()
        # print("The plotted rolling standard deviation using a 21 trading day window for all portfolios:")
        # Combined_PCT_Returns.rolling(window=21).std().plot(
        #     kind='line',
        #     figsize=(20, 12),
        #     title="The plotted rolling standard deviation using a 21 trading day",
        #     fontsize=12,
        #     #subplots=True,
        #     grid=True);


        # The calculated annualized Sharpe Ratios and the accompanying bar plot visualization:
        # print("The calculated annualized Sharpe Ratios and the accompanying bar plot visualization:")
        # print("====================================================================================")
        # print()
        # # Calculate annualized Sharpe Ratios
        # Anunualized_Sharpe_Ratios = (Combined_PCT_Returns.mean() * 252) / (Combined_PCT_Returns.std() * np.sqrt(252))
        # print(Anunualized_Sharpe_Ratios)
        # print()
        # print("Bar Plot for Sharp Ratio")
        # # Visualize the sharpe ratios as a bar plot
        # Anunualized_Sharpe_Ratios.plot(
        #     kind='bar',
        #     title="Sharpe Ratios - Return to Risk",
        #     figsize=(18,12),
        #     fontsize=12,
        #     #subplots=True,
        #     grid=True);


        # Construct a correlation table
        # print("A correlation between portfolios")
        # print("================================================================")
        # Correlation = Combined_PCT_Returns.corr()
        # Correlation
        # sns.heatmap(Correlation, vmin=-1, vmax=1);
