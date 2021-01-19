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
import random

from dotenv import load_dotenv
from MCForecastTools import MCSimulation

from ..datastructures.StockInfoContainer import StockInfoContainer

class AnalysisMethod:


    def __init__(self, analysis_method_name):
        # Constants
        self.__const_analysis_method = "PriceForecasting"


    def get_const_analysis_method_str(self):
        return self.__const_analysis_method


    def analyze(self, stock_info_container):
        raise NotImplementedError


class PriceForecaster(AnalysisMethod):


    def __init__(self):
        super().__init__("PriceForecasting")
        # Constants
        self.__const_analysis_method = "PriceForecasting"

        # Load environment variables
        load_dotenv()
        self.__kraken_public_key = os.getenv("KRAKEN_API_KEY")
        self.__kraken_secret_key = os.getenv("KRAKEN_SECRET_KEY")


    def analyze(self, stock_info_container):

        for stock_ticker in stock_info_container.get_all_tickers():
            score = random.random()  # TODO











            stock_info_container.add_stock_score(stock_ticker, self.__const_analysis_method, score)

        return stock_info_container


    def __generate_price_prediction(self, stock_info_container):



    def generate_price_prediction_2(self, stock_info_container):

        # Concatenate all DataFrames into a single DataFrame
        # stock_price_history = pd.concat([ BTC_df, ETH_df, XRP_df ], axis="columns", join="inner")
        # stock_price_history.sort_index(inplace=True)

        stock_price_history = None

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
        import pandas as pd
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
        model = ARMA(stock_price_history_pctchange.values, order=(1, 1))
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
        BTC_csv=None
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
        plt = Predictions_Results[:20].plot(
            figsize=(20, 5),
            fontsize=20,
            rot=70,
            subplots=True,
            grid=True);
        plt.title(label="BitCoin's Return vs. Predicted Returns for the next 20 Days", fontsize=25);












        # --------------------------------------------------------------------------
        # Machine Learning
        # --------------------------------------------------------------------------
        #
        # # Initial imports
        # import math
        # import pandas_datareader as web
        # import numpy as np
        # import pandas as pd
        # from sklearn.preprocessing import MinMaxScaler
        # from keras.models import Sequential
        # from keras.layers import Dense, LSTM
        # import matplotlib.pyplot as plt
        # plt.style.use('fivethirtyeight')
        #
        # # Get the stock data using yahoo source
        # df = web.DataReader('AAPL', data_source='yahoo', start='2016-01-01', end='2021-01-14')
        # df
        #
        # # Create a new dataframe with only the 'Close Column'
        # data = df.filter(['Close'])
        # # Convert the dataframe to a numpy array
        # dataset = data.values
        # # Get the number of rows to train the model on
        # training_data_len = math.ceil(len(dataset) * .8)
        #
        # training_data_len
        # # Scale the Data
        # scaler = MinMaxScaler(feature_range=(0, 1))
        # scaled_data = scaler.fit_transform(dataset)
        #
        # scaled_data
        #
        # # Create the training data set
        # # Create the scaled training data set
        # train_data = scaled_data[0:training_data_len, :]
        # # Split the data into x_train and y_train data sets
        # x_train = []
        # y_train = []
        #
        # for i in range(60, len(train_data)):
        #     x_train.append(train_data[i - 60:i, 0])
        #     y_train.append(train_data[i, 0])
        #     if i <= 61:
        #         print(x_train)
        #         print(y_train)
        #         print()
        #
        # x_train, y_train = np.array(x_train), np.array(y_train)
        #
        # x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        #
        # # Build the LSTM Model
        # model = Sequential()
        # model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        # model.add(LSTM(50, return_sequences=False))
        # model.add(Dense(25))
        # model.add(Dense(1))
        #
        # model.compile(optimizer='adam', loss='mean_squared_error')
        #
        # model.fit(x_train, y_train, batch_size=1, epochs=6)
        #
        # # Create the testing data set
        # # Create a new array containing scaled values from index 1266 to 953
        # test_data = scaled_data[training_data_len - 60:, :]
        # # Create the data sets x_test and y_test
        # x_test = []
        # y_test = dataset[training_data_len:, :]
        # for i in range(60, len(test_data)):
        #     x_test.append(test_data[i - 60:i, 0])
        #
        # x_test = np.array(x_test)
        #
        # x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        # # Get the models predicted price values
        # predictions = model.predict(x_test)
        # predictions = scaler.inverse_transform(predictions)
        #
        # # Get the root mean squared error (RMSE)
        # rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
        # rmse
        #
        # # Plot the data
        # train = data[:training_data_len]
        # valid = data[training_data_len:]
        # valid['Predictions'] = predictions
        # # Visualize the data
        # plt.figure(figsize=(16, 8))
        # plt.title('LSTM Model')
        # plt.xlabel('Date', fontsize=18)
        # plt.ylabel('Close Price USD ($)', fontsize=18)
        # plt.plot(train['Close'])
        # plt.plot(valid[['Close', 'Predictions']])
        # plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
        # plt.show()
        #
        # # Get the quote
        # apple_quote = web.DataReader('AAPL', data_source='yahoo', start='2016-01-01', end='2021-01-14')
        # # Create a new dataframe
        # new_df = apple_quote.filter(['Close'])
        # # Get the last 60 days closing price values and convert the dataframe to an array
        # last_60_days = new_df[-60:].values
        # # Scale the data to be values between 0 and 1
        # last_60_days_scaled = scaler.transform(last_60_days)
        # # Create an empty list
        # X_test = []
        # # Append the past 60 days
        # X_test.append(last_60_days_scaled)
        # # Convert the X_test data set to numpy array
        # X_test = np.array(X_test)
        # # Reshape the data
        # X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        # # Get the predicted scaled price
        # pred_price = model.predict(X_test)
        # # Undo the Scaling
        # pred_price = scaler.inverse_transform(pred_price)
        # print(pred_price)
        #
        # valid.forecast(steps=10)[2]

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