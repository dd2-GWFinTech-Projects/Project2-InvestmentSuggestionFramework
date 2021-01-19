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
from matplotlib import pyplot as plt
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARIMA
import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
from ..priceanalysis.MCForecastTools import MCSimulation
from ..datastructures.StockInfoContainer import StockInfoContainer
from ..datastructures.AnalysisMethod import AnalysisMethod

class PriceForecaster(AnalysisMethod):


    def __init__(self):
        super().__init__("PriceForecasting")
        self.__const_analysis_method = "PriceForecasting"

        # Load environment variables
        load_dotenv()
        self.__kraken_public_key = os.getenv("KRAKEN_API_KEY")
        self.__kraken_secret_key = os.getenv("KRAKEN_SECRET_KEY")


    def analyze(self, stock_info_container):

        stock_info_container = self.__generate_price_prediction(stock_info_container)
        # for stock_ticker in stock_info_container.get_all_tickers():
            # score = self.__generate_price_prediction(stock_info_container)
            # stock_info_container.add_stock_score(stock_ticker, self.__const_analysis_method, score)

        return stock_info_container



    def __generate_price_prediction(self, stock_info_container):

        # --------------------------------------------------------------------------
        # Clean prices dataframe
        # --------------------------------------------------------------------------

        stock_price_history = stock_info_container.get_all_price_history()
        stock_price_history = self.__clean_dataframe(stock_price_history)
        stock_price_pct_change = stock_price_history.pct_change()
        stock_price_pct_change = stock_price_pct_change.dropna()

        # --------------------------------------------------------------------------
        # ARMA prediction and compute score
        # --------------------------------------------------------------------------

        # ARMA prediction
        pctchange_results_arma = self.__compute_forecast_arma(stock_price_pct_change, order=(1,1), num_steps=10)
        predicted_values_arma = self.__compute_values_from_pctchange(stock_price_history, pctchange_results_arma)

        # Compute score
        stock_info_container = self.__compute_score_from_prediction(stock_info_container, stock_price_history, predicted_values_arma, "ARMA")

        # --------------------------------------------------------------------------
        # ARIMA prediction and compute score
        # --------------------------------------------------------------------------

        # ARIMA prediction and compute score
        pctchange_results_arima = self.__compute_forecast_arima(stock_price_pct_change, order=(1, 1, 1), num_steps=10)
        predicted_values_arima = self.__compute_values_from_pctchange(stock_price_history, pctchange_results_arima)

        # Compute score
        stock_info_container = self.__compute_score_from_prediction(stock_info_container, stock_price_history, predicted_values_arima, "ARIMA")

        return stock_info_container


    def __compute_forecast_arma(self, stock_price_history, order=(1,1), num_steps=10):
        results_df = pd.DataFrame()
        for stock_ticker in stock_price_history.columns:
            model = ARMA(stock_price_history[stock_ticker].values, order=order)
            results = model.fit()
            results_df[stock_ticker] = results.forecast(steps=num_steps)[0]
        return results_df

    def __compute_forecast_arima(self, stock_price_history, order=(1,1), num_steps=10):
        # Lag 1 order=(1,1)
        # Lag 2 order=(2,1,1)
        results_df = pd.DataFrame()
        for stock_ticker in stock_price_history.columns:
            model = ARIMA(stock_price_history[stock_ticker].values, order=order)
            results = model.fit()
            results_df[stock_ticker] = results.forecast(steps=num_steps)[0]
        return results_df

    def __clean_dataframe(self, stock_price_history):
        return stock_price_history.sort_index()

    def __compute_values_from_pctchange(self, stock_price_history, pctchange_prediction):
        predicted_values = pd.DataFrame()
        for stock_ticker in stock_price_history.columns:
            last_actual_value = stock_price_history[stock_ticker].tail(1).iloc[0]
            predicted_values[stock_ticker] = pctchange_prediction[stock_ticker] + last_actual_value
        return predicted_values

    def __compute_score_from_prediction(self, stock_info_container, stock_price_history, predicted_values, sub_analysis_method_str):
        for stock_ticker in stock_price_history.columns:
            last_actual_value = stock_price_history[stock_ticker].tail(1).iloc[0]
            last_predicted_value = predicted_values[stock_ticker].tail(1).iloc[0]
            score = self.__compute_score_from_prediction_scalar(last_actual_value, last_predicted_value)
            stock_info_container.add_stock_score(stock_ticker, score, self.__const_analysis_method + "." + sub_analysis_method_str)
        return stock_info_container

    def __compute_score_from_prediction_scalar(self, last_actual_value, last_predicted_value):
        return (last_predicted_value - last_actual_value) / last_actual_value


    #
    # def __abc(self):
    #     # --------------------------------------------------------------------------
    #     # ## Risk
    #     # --------------------------------------------------------------------------
    #
    #     # --------------------------------------------------------------------------
    #     # ## Standard Deviation
    #     # --------------------------------------------------------------------------
    #     #
    #     # # Daily Standard Deviations for each portfolio.
    #     # import pandas as pd
    #     # Combined_PCT_Returns_STD = pd.DataFrame(stock_price_history_pctchange.std())
    #     # Combined_PCT_Returns_STD.columns = ["Daily Standard Deviation"]
    #     #
    #     #
    #     # # Determine which portfolios are riskier than the S&P 500
    #     # # print("The Below Portfolios are Riskier than S&P 500")
    #     # Riskier_GSPC = Combined_PCT_Returns_STD.loc[Combined_PCT_Returns_STD["Daily Standard Deviation"] > Combined_PCT_Returns_STD.loc["S&P 500", "Daily Standard Deviation"]]
    #     #
    #     # # --------------------------------------------------------------------------
    #     # # ## Exponentially Weighted Moving Average
    #     # # --------------------------------------------------------------------------
    #     #
    #     # # Calculate a rolling window using the exponentially weighted moving average.
    #     # stock_price_history_pctchange.ewm(halflife = 21).std()
    #     #
    #     # # --------------------------------------------------------------------------
    #     # # ## ARMA Analysis
    #     # # --------------------------------------------------------------------------
    #     #
    #     # # Import the ARMA model
    #     # from statsmodels.tsa.arima_model import ARMA
    #     # # Create the ARMA model using the return values and the order
    #     # # For the order parameter, the first 1 indicates the number of AR lags
    #     # # For the order parameter, the second 1 indicates the number of MA lags
    #     # model = ARMA(stock_price_history_pctchange.values, order=(1, 1))
    #     # # Fit the model to the data
    #     # predicted_values = model.fit()
    #     # # Create the ARMA model using the return values and the order
    #     # # For the order parameter, the first 1 indicates the number of AR lags
    #     # # For the order parameter, the second 1 indicates the number of MA lags
    #     # model_ARMA_2 = ARMA(AAPL_close_df.values, order=(1, 1))
    #     # # Fit the model to the data
    #     # results_close = model_ARMA_2.fit()
    #     #
    #     # predicted_values.forecast(steps=10)[0]
    #     #
    #     # import arch as arch
    #     # import warnings
    #     # warnings.filterwarnings('ignore')
    #     # # Create a series using "Close" price percentage returns, drop any NaNs, and check the predicted_values:
    #     # # (Make sure to multiply the pct_change() predicted_values by *100)
    #     # BTC_csv=None
    #     # BTC_csv['Return'] = BTC_csv.Close.pct_change() * 100
    #     # BTC_csv['Lagged_Return'] = BTC_csv['Return'].shift()
    #     # BTC_csv = BTC_csv.dropna()
    #     # BTC_csv.tail()
    #     #
    #     # # Create a train/test split for the data using 2017-2018 for training and 2019 for testing
    #     # train = BTC_csv['2017':'2019']
    #     # test = BTC_csv['2020']
    #     # # Create four DataFrames:
    #     # # X_train (training set using just the independent variables), X_test (test set of of just the independent variables)
    #     # # Y_train (training set using just the "y" variable, i.e., "Futures Return"), Y_test (test set of just the "y" variable):
    #     # X_train = train["Lagged_Return"].to_frame()
    #     # y_train = train["Return"]
    #     # X_test = test["Lagged_Return"].to_frame()
    #     # y_test = test["Return"]
    #     #
    #     # # Create a Linear Regression model and fit it to the training data
    #     # from sklearn.linear_model import LinearRegression
    #     #
    #     # # Fit a SKLearn linear regression using just the training set (X_train, Y_train):
    #     # model_LR = LinearRegression()
    #     # model_LR.fit(X_train, y_train)
    #     #
    #     # # Make a prediction of "y" values using just the test dataset
    #     # BTC_predictions = model_LR.predict(X_test)
    #     # # Assemble actual y data (Y_test) with predicted y data (from just above) into two columns in a DataFrame:
    #     # Predictions_Results = y_test.to_frame()
    #     # Predictions_Results["Predicted Return"] = BTC_predictions
    #     #
    #     # # Plot the first 20 predictions vs the true values
    #     # plt = Predictions_Results[:20].plot(
    #     #     figsize=(20, 5),
    #     #     fontsize=20,
    #     #     rot=70,
    #     #     subplots=True,
    #     #     grid=True);
    #     # plt.title(label="BitCoin's Return vs. Predicted Returns for the next 20 Days", fontsize=25);
    #
    #     # --------------------------------------------------------------------------
    #     # Machine Learning
    #     # --------------------------------------------------------------------------
    #     #
    #     # # Initial imports
    #     # import math
    #     # import pandas_datareader as web
    #     # import numpy as np
    #     # import pandas as pd
    #     # from sklearn.preprocessing import MinMaxScaler
    #     # from keras.models import Sequential
    #     # from keras.layers import Dense, LSTM
    #     # import matplotlib.pyplot as plt
    #     # plt.style.use('fivethirtyeight')
    #     #
    #     # # Get the stock data using yahoo source
    #     # df = web.DataReader('AAPL', data_source='yahoo', start='2016-01-01', end='2021-01-14')
    #     # df
    #     #
    #     # # Create a new dataframe with only the 'Close Column'
    #     # data = df.filter(['Close'])
    #     # # Convert the dataframe to a numpy array
    #     # dataset = data.values
    #     # # Get the number of rows to train the model on
    #     # training_data_len = math.ceil(len(dataset) * .8)
    #     #
    #     # training_data_len
    #     # # Scale the Data
    #     # scaler = MinMaxScaler(feature_range=(0, 1))
    #     # scaled_data = scaler.fit_transform(dataset)
    #     #
    #     # scaled_data
    #     #
    #     # # Create the training data set
    #     # # Create the scaled training data set
    #     # train_data = scaled_data[0:training_data_len, :]
    #     # # Split the data into x_train and y_train data sets
    #     # x_train = []
    #     # y_train = []
    #     #
    #     # for i in range(60, len(train_data)):
    #     #     x_train.append(train_data[i - 60:i, 0])
    #     #     y_train.append(train_data[i, 0])
    #     #     if i <= 61:
    #     #         print(x_train)
    #     #         print(y_train)
    #     #         print()
    #     #
    #     # x_train, y_train = np.array(x_train), np.array(y_train)
    #     #
    #     # x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    #     #
    #     # # Build the LSTM Model
    #     # model = Sequential()
    #     # model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    #     # model.add(LSTM(50, return_sequences=False))
    #     # model.add(Dense(25))
    #     # model.add(Dense(1))
    #     #
    #     # model.compile(optimizer='adam', loss='mean_squared_error')
    #     #
    #     # model.fit(x_train, y_train, batch_size=1, epochs=6)
    #     #
    #     # # Create the testing data set
    #     # # Create a new array containing scaled values from index 1266 to 953
    #     # test_data = scaled_data[training_data_len - 60:, :]
    #     # # Create the data sets x_test and y_test
    #     # x_test = []
    #     # y_test = dataset[training_data_len:, :]
    #     # for i in range(60, len(test_data)):
    #     #     x_test.append(test_data[i - 60:i, 0])
    #     #
    #     # x_test = np.array(x_test)
    #     #
    #     # x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    #     # # Get the models predicted price values
    #     # predictions = model.predict(x_test)
    #     # predictions = scaler.inverse_transform(predictions)
    #     #
    #     # # Get the root mean squared error (RMSE)
    #     # rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
    #     # rmse
    #     #
    #     # # Plot the data
    #     # train = data[:training_data_len]
    #     # valid = data[training_data_len:]
    #     # valid['Predictions'] = predictions
    #     # # Visualize the data
    #     # plt.figure(figsize=(16, 8))
    #     # plt.title('LSTM Model')
    #     # plt.xlabel('Date', fontsize=18)
    #     # plt.ylabel('Close Price USD ($)', fontsize=18)
    #     # plt.plot(train['Close'])
    #     # plt.plot(valid[['Close', 'Predictions']])
    #     # plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
    #     # plt.show()
    #     #
    #     # # Get the quote
    #     # apple_quote = web.DataReader('AAPL', data_source='yahoo', start='2016-01-01', end='2021-01-14')
    #     # # Create a new dataframe
    #     # new_df = apple_quote.filter(['Close'])
    #     # # Get the last 60 days closing price values and convert the dataframe to an array
    #     # last_60_days = new_df[-60:].values
    #     # # Scale the data to be values between 0 and 1
    #     # last_60_days_scaled = scaler.transform(last_60_days)
    #     # # Create an empty list
    #     # X_test = []
    #     # # Append the past 60 days
    #     # X_test.append(last_60_days_scaled)
    #     # # Convert the X_test data set to numpy array
    #     # X_test = np.array(X_test)
    #     # # Reshape the data
    #     # X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    #     # # Get the predicted scaled price
    #     # pred_price = model.predict(X_test)
    #     # # Undo the Scaling
    #     # pred_price = scaler.inverse_transform(pred_price)
    #     # print(pred_price)
    #     #
    #     # valid.forecast(steps=10)[2]
    #
    #     # return stock_info_container
    #
    #
    # def __calculate_adjusted_prices(self, df, close):
    #     # """ Vectorized approach for calculating the adjusted prices for the
    #     # specified column in the provided DataFrame. This creates a new column
    #     # called 'adj_<column name>' with the adjusted prices. This function requires
    #     # that the DataFrame have columns with dividend and split_ratio values.
    #     #
    #     # :param df: DataFrame with raw prices along with dividend and split_ratio
    #     #     values
    #     # :param column: String of which price column should have adjusted prices
    #     #     created for it
    #     # :return: DataFrame with the addition of the adjusted price column
    #     # """
    #     # adj_column = 'adj_' + close
    #     #
    #     # # Reverse the DataFrame order, sorting by date in descending order
    #     # Data.sort_index(ascending=False, inplace=True)
    #     #
    #     # price_col = Data[close].values
    #     # split_col = Data['split_ratio'].values
    #     # dividend_col = Data['dividend'].values
    #     # adj_price_col = np.zeros(len(Data.index))
    #     # adj_price_col[0] = price_col[0]
    #     #
    #     # for i in range(1, len(price_col)):
    #     #     adj_price_col[i] = round((adj_price_col[i - 1] + adj_price_col[i - 1] *
    #     #                (((price_col[i] * split_col[i - 1]) -
    #     #                  price_col[i - 1] -
    #     #                  dividend_col[i - 1]) / price_col[i - 1])), 4)
    #     #
    #     # Data[adj_column] = adj_price_col
    #     #
    #     # # Change the DataFrame order back to dates ascending
    #     # Data.sort_index(ascending=True, inplace=True)
    #     #
    #     # return Data
    #     return df
    #
    # def __compute_beta(self):
    #     # Covariance_Apple = Data["Adj_Close"].rolling(window=21).cov(Data_1["S&P500_Adj_Close"])
    #     # Variance_Apple = Data_1["S&P500_Adj_Close"].rolling(window=21).var()
    #     # Beta_Apple = Covariance_Apple / Variance_Apple
    #     return None
    #
    # def __compute_correlation(self):
    #     # Correlation = Combined_Returns.corr()
    #     return None
    #
    #
    #
    # # def __compute_linear_regression(self, stock_price_history):
    # #
    # #     # Create a train/test split for the data using 2017-2018 for training and 2019 for testing
    # #     num_days = stock_price_history.shape[0]
    # #     train = stock_price_history.loc[0:(0.7 * num_days)]
    # #     test = stock_price_history.loc[(0.7 * num_days):num_days]
    # #
    # #     # Create four DataFrames:
    # #     # X_train (training set using just the independent variables), X_test (test set of of just the independent variables)
    # #     # Y_train (training set using just the "y" variable, i.e., "Futures Return"), Y_test (test set of just the "y" variable):
    # #     X_train = train["Lagged_Return"].to_frame()
    # #     y_train = train["Return"]
    # #     X_test = test["Lagged_Return"].to_frame()
    # #     y_test = test["Return"]
    # #
    # #     # Create a Linear Regression model and fit it to the training data
    # #     from sklearn.linear_model import LinearRegression
    # #
    # #     # Fit a SKLearn linear regression using just the training set (X_train, Y_train):
    # #     model_LR = LinearRegression()
    # #     model_LR.fit(X_train, y_train)
