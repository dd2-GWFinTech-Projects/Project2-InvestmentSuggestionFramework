# --------------------------------------------------------------------------
# Time Series Basics
# --------------------------------------------------------------------------

import os
import warnings

# Initial imports
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARMA

warnings.filterwarnings('ignore')

from dotenv import load_dotenv
from ..priceanalysis.MCForecastTools import MCSimulation
from main.lib.datastructures.AnalysisMethod import AnalysisMethod

class PriceForecaster(AnalysisMethod):


    def __init__(self):
        super().__init__("PriceForecasting")
        self.__const_analysis_method = "PriceForecasting"

        # Load environment variables
        self.__kraken_public_key = "/v0eRFBimcTXNmjv5vUdNlppVKdcdlWCvxFNubBSmnlkttijwqwodoyM"
        self.__kraken_secret_key = "Ca2phfU4uhOBSveZTnFTHMQfEAf23Ng2Ojvu71IhijHMxpPsWClFXv59lCcw5kcqOqkcGT9GsM2Sa+Mje45mtA=="


    def analyze(self, stock_info_container):

        # --------------------------------------------------------------------------
        # Clean prices dataframe
        # --------------------------------------------------------------------------

        stock_price_history = stock_info_container.get_all_price_history()
        stock_price_history = self.__clean_dataframe(stock_price_history)
        stock_price_pct_change = stock_price_history.pct_change()
        # stock_price_pct_change = stock_price_pct_change.dropna()

        # --------------------------------------------------------------------------
        # ARMA prediction and compute score
        # --------------------------------------------------------------------------

        # ARMA prediction
        pctchange_results_arma = self.__compute_forecast_arma(stock_info_container, stock_price_pct_change, order=(1,1), num_steps=10)
        predicted_values_arma = self.__compute_values_from_pctchange(stock_info_container, stock_price_history, pctchange_results_arma)

        # Compute score
        stock_info_container = self.__compute_score_from_prediction(stock_info_container, stock_price_history, predicted_values_arma, "ARMA")

        # --------------------------------------------------------------------------
        # ARIMA prediction and compute score
        # --------------------------------------------------------------------------

        # ARIMA prediction and compute score
        pctchange_results_arima = self.__compute_forecast_arima(stock_info_container, stock_price_pct_change, order=(1, 1, 1), num_steps=10)
        predicted_values_arima = self.__compute_values_from_pctchange(stock_info_container, stock_price_history, pctchange_results_arima)

        # Compute score
        stock_info_container = self.__compute_score_from_prediction(stock_info_container, stock_price_history, predicted_values_arima, "ARIMA")

        return stock_info_container


    def __compute_forecast_arma(self, stock_info_container, stock_price_history, order=(1,1), num_steps=10):
        results_df = pd.DataFrame()
        for stock_ticker in stock_info_container.get_all_tickers():
            stock_price_history_individual = stock_price_history[stock_ticker].dropna()
            model = ARMA(stock_price_history_individual.values, order=order)
            results = model.fit()
            results_df[stock_ticker] = results.forecast(steps=num_steps)[0]
        return results_df


    def __compute_forecast_arima(self, stock_info_container, stock_price_history, order=(1,1), num_steps=10):
        # Lag 1 order=(1,1)
        # Lag 2 order=(2,1,1)
        results_df = pd.DataFrame()
        for stock_ticker in stock_info_container.get_all_tickers():
            stock_price_history_individual = stock_price_history[stock_ticker].dropna()
            model = ARIMA(stock_price_history_individual.values, order=order)
            results = model.fit()
            results_df[stock_ticker] = results.forecast(steps=num_steps)[0]
        return results_df


    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------


    def __clean_dataframe(self, stock_price_history):
        return stock_price_history.sort_index()


    def __compute_values_from_pctchange(self, stock_info_container, stock_price_history, pctchange_prediction):
        predicted_values = pd.DataFrame()
        for stock_ticker in stock_info_container.get_all_tickers():
            last_actual_value = stock_price_history[stock_ticker].tail(1).iloc[0]
            predicted_values[stock_ticker] = pctchange_prediction[stock_ticker] + last_actual_value
        return predicted_values


    def __compute_score_from_prediction(self, stock_info_container, stock_price_history, predicted_values, sub_analysis_method_str):
        for stock_ticker in stock_info_container.get_all_tickers():
            last_actual_value = stock_price_history[stock_ticker].tail(1).iloc[0]
            last_predicted_value = predicted_values[stock_ticker].tail(1).iloc[0]
            score = self.__compute_score_from_prediction_scalar(last_actual_value, last_predicted_value)
            stock_info_container.add_stock_raw_score(stock_ticker, score, self.__const_analysis_method + "." + sub_analysis_method_str)
        return stock_info_container


    def __compute_score_from_prediction_scalar(self, last_actual_value, last_predicted_value):
        return 100 * (last_predicted_value - last_actual_value) / last_actual_value
