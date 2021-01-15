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

from ..datastructures.StockInfoContainer import StockInfoContainer


class PriceForecaster:

    def __init__(self):

        # --------------------------------------------------------------------------
        # Load environment variables
        # --------------------------------------------------------------------------

        load_dotenv()

        # Import environment variables
        Kraken_Public_Key = os.getenv("KRAKEN_API_KEY")
        Kraken_Secret_Key = os.getenv("KRAKEN_SECRET_KEY")

    def generate_price_prediction(self, stock_info_list):

        stock_info_container = StockInfoContainer()

        # Concatenate all DataFrames into a single DataFrame
        # stock_price_history = pd.concat([ BTC_df, ETH_df, XRP_df ], axis="columns", join="inner")
        # stock_price_history.sort_index(inplace=True)

        # stock_price_history

        # Format the DateTime to remove Time
        stock_price_history.index = stock_price_history.index.strftime("%Y-%m-%d")


        # Pick all Stocks volumes
        AAPL_volume_df = stock_price_history["AAPL"]["volume"]


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
        AAPL_close_df = stock_price_history["AAPL"]["close"]

        # Rename Column
        AAPL_close_df.columns = ["Apple"]





        # --------------------------------------------------------------------------
        # ## Combining Daily Returns
        # --------------------------------------------------------------------------

        # Calculate Daily Returns for all the stocks
        stock_price_history_pctchange = stock_price_history.pct_change()  #pd.concat([ BXP_df, PLD_df, NOC_df, BA_df, PYPL_df, SQ_df, JNJ_df, PFE_df, TSLA_df, AAPL_df, SPY_df ], axis="columns", join="inner")
        stock_price_history_pctchange.sort_index(inplace=True)

        # Drop nulls
        stock_price_history_pctchange.dropna(inplace=True)


        # Rename Column
        # stock_price_history_pctchange.columns = ["Boston Properties", "Prologis", "Northrop Grumman", "Boeing", "Paypal Holdings", "Square", "Johnson & Johnson", "Pfizer", "Tesla", "Apple", "S&P 500"]
        stock_price_history_pctchange.tail()

        # --------------------------------------------------------------------------
        # ## Daily Returns
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # ## Risk
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # ## Standard Deviation
        # --------------------------------------------------------------------------

        # Daily Standard Deviations for each portfolio.
        Combined_PCT_Returns_STD = pd.DataFrame(stock_price_history_pctchange.std())
        Combined_PCT_Returns_STD.columns = ["Daily Standard Deviation"]


        # Determine which portfolios are riskier than the S&P 500
        # print("The Below Portfolios are Riskier than S&P 500")
        Riskier_GSPC = Combined_PCT_Returns_STD.loc[Combined_PCT_Returns_STD["Daily Standard Deviation"] > Combined_PCT_Returns_STD.loc["S&P 500", "Daily Standard Deviation"]]

        # --------------------------------------------------------------------------
        # ## Exponentially Weighted Moving Average
        # --------------------------------------------------------------------------

        # Calculate a rolling window using the exponentially weighted moving average.
        stock_price_history_pctchange.ewm(halflife = 21).std()

        # --------------------------------------------------------------------------
        # ## ARMA Analysis
        # --------------------------------------------------------------------------

        # Import the ARMA model
        from statsmodels.tsa.arima_model import ARMA
        # Create the ARMA model using the return values and the order
        # For the order parameter, the first 1 indicates the number of AR lags
        # For the order parameter, the second 1 indicates the number of MA lags
        model = ARMA(AAPL_close_df_pct.values, order=(1, 1))
        # Fit the model to the data
        results = model.fit()
        # Create the ARMA model using the return values and the order
        # For the order parameter, the first 1 indicates the number of AR lags
        # For the order parameter, the second 1 indicates the number of MA lags
        model_ARMA_2 = ARMA(AAPL_close_df.values, order=(1, 1))
        # Fit the model to the data
        results_close = model_ARMA_2.fit()

        results.forecast(steps=10)[0]

        # --------------------------------------------------------------------------
        # ARIMA Analysis
        # --------------------------------------------------------------------------

        from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
        from statsmodels.tsa.arima_model import ARIMA
        # Create an ARIMA model
        model = ARIMA(AAPL_close_df.values, order=(1, 1, 1))
        # Fit the model to the data
        results_ARIMA = model.fit()
        # Print the model summary
        results_ARIMA.summary()

        results_ARIMA.forecast(steps=10)[0]




        # --------------------------------------------------------------------------
        # Linear Regression Analysis
        # --------------------------------------------------------------------------

        import arch as arch
        import warnings
        warnings.filterwarnings('ignore')
        # Create a series using "Close" price percentage returns, drop any NaNs, and check the results:
        # (Make sure to multiply the pct_change() results by *100)
        BTC_csv['Return'] = BTC_csv.Close.pct_change() * 100
        BTC_csv['Lagged_Return'] = BTC_csv['Return'].shift()
        BTC_csv = BTC_csv.dropna()
        BTC_csv.tail()

        # Create a train/test split for the data using 2017-2018 for training and 2019 for testing
        train = BTC_csv['2017':'2019']
        test = BTC_csv['2020']
        # Create four DataFrames:
        # X_train (training set using just the independent variables), X_test (test set of of just the independent variables)
        # Y_train (training set using just the "y" variable, i.e., "Futures Return"), Y_test (test set of just the "y" variable):
        X_train = train["Lagged_Return"].to_frame()
        y_train = train["Return"]
        X_test = test["Lagged_Return"].to_frame()
        y_test = test["Return"]

        # Create a Linear Regression model and fit it to the training data
        from sklearn.linear_model import LinearRegression

        # Fit a SKLearn linear regression using just the training set (X_train, Y_train):
        model_LR = LinearRegression()
        model_LR.fit(X_train, y_train)

        # Make a prediction of "y" values using just the test dataset
        BTC_predictions = model_LR.predict(X_test)
        # Assemble actual y data (Y_test) with predicted y data (from just above) into two columns in a DataFrame:
        Predictions_Results = y_test.to_frame()
        Predictions_Results["Predicted Return"] = BTC_predictions

        # Plot the first 20 predictions vs the true values
        Predictions_Results[:20].plot(
            figsize=(20, 5),
            fontsize=20,
            rot=70,
            subplots=True,
            grid=True);
        plt.title(label="BitCoin's Return vs. Predicted Returns for the next 20 Days", fontsize=25);




        return stock_info_container






    def calculate_adjusted_prices(Data, close):
        """ Vectorized approach for calculating the adjusted prices for the
        specified column in the provided DataFrame. This creates a new column
        called 'adj_<column name>' with the adjusted prices. This function requires
        that the DataFrame have columns with dividend and split_ratio values.

        :param df: DataFrame with raw prices along with dividend and split_ratio
            values
        :param column: String of which price column should have adjusted prices
            created for it
        :return: DataFrame with the addition of the adjusted price column
        """
        adj_column = 'adj_' + close

        # Reverse the DataFrame order, sorting by date in descending order
        Data.sort_index(ascending=False, inplace=True)

        price_col = Data[close].values
        split_col = Data['split_ratio'].values
        dividend_col = Data['dividend'].values
        adj_price_col = np.zeros(len(Data.index))
        adj_price_col[0] = price_col[0]

        for i in range(1, len(price_col)):
            adj_price_col[i] = round((adj_price_col[i - 1] + adj_price_col[i - 1] *
                       (((price_col[i] * split_col[i - 1]) -
                         price_col[i - 1] -
                         dividend_col[i - 1]) / price_col[i - 1])), 4)

        Data[adj_column] = adj_price_col

        # Change the DataFrame order back to dates ascending
        Data.sort_index(ascending=True, inplace=True)

        return Data