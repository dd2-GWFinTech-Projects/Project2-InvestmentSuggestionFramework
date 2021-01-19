import numpy as np
import random
from ..datastructures.AnalysisMethod import AnalysisMethod


class IndustryInfo:
    def __init__(self, has_dividend, use_dcf, use_cap_rate_market_model):
        self.has_dividend = has_dividend
        self.use_dcf = use_dcf
        self.use_cap_rate_market_model = use_cap_rate_market_model


class ValuationCalculator(AnalysisMethod):


    def __init__(self, debug_level=0):
        super().__init__("Valuation")
        self.__const_analysis_method = "Valuation"
        self.__debug_level = 0
        # Source: https://www.valentiam.com/newsandinsights/ebitda-multiples-by-industry
        self.__industry_multiples = {
            "Healthcare information and technology": 24.81,
            "Airlines": 8.16,
            "Drugs, biotechnology": 13.29,
            "Hotels and casinos": 12.74,
            "Retail, general": 12.21,
            "Retail, food": 8.93,
            "Utilities, excluding water": 14.13,
            "Homebuilding": 10.95,
            "Medical equipment and supplies": 22.67,
            "Oil and gas, exploration and production": 4.89,
            "Telecom, equipment (phones & handheld devices)": 13.42,
            "Professional information services (big data)": 26.35,
            "Software, system & application": 24.00,
            "Wireless telecommunications services": 6.64
        }
        self.__industry_info = {
            "Technology": IndustryInfo(False, True, False)
        }
        # Constants
        self.__const_analysis_method = "Valuation"


    def analyze(self, stock_info_container):
        stock_info_container = self.__compute_valuation_scores(stock_info_container)
        return stock_info_container


    def __compute_valuation_scores(self, stock_info_container):

        stock_price_history = stock_info_container.get_all_price_history()

        for stock_ticker in stock_info_container.get_all_tickers():
            industry = stock_info_container.get_all_financial_metadata()[stock_ticker]["industry"]
            valuation = self.__compute_valuation(stock_ticker, stock_info_container.get_all_financial_metadata())
            current_price = stock_price_history[stock_ticker].tail(1).iloc[0]
            score = self.__compute_score(current_price, valuation)

        return None


    def __compute_valuation(self, stock_ticker, industry, all_financial_metadata):
        if self.__industry_info[industry].has_dividend:
            ticker = None
            r = None
            g = None
            return self.compute_value__dividend_discount_model(ticker, r, g)
        elif self.__industry_info[industry].use_dcf:
            ebitda_projection = None
            wacc = None
            return self.compute_value__dcf(ebitda_projection, wacc)
        elif self.__industry_info[industry].use_cap_rate_market_model:  # Need cap rate; prefer real estate industry
            industry_multiples = None
            market_cap = None
            capitalization_rate = None
            return self.compute_value__cap_rate_market_model(industry_multiples, market_cap, capitalization_rate)
        else:
            equity_value = None
            expected_ebitda = None
            ebitda = None
            return self.compute_market_value(equity_value, expected_ebitda, ebitda)


    def __compute_score(self, current_price, valuation):
        return 100.0 * (valuation - current_price) / current_price


    # --------------------------------------------------------------------------
    # Dividend Discount Model
    # --------------------------------------------------------------------------


    # TODO Correlate industries to changing dividends
    def compute_value__dividend_discount_model(self,
        ticker,
        #dividend_yield_fractional, # Dividend yield
        #npv, # Net present value
        #wacc, # Weighted cost of capital
        #eps, # Earnings per share
        #market_cap,
        r,  # Cost of equity capital == interest rate
        g  # Growth rate == eps growth
    ):
        dividend_next_year = np.nan
        npv = dividend_next_year / (r - g)
        return npv


    # --------------------------------------------------------------------------
    # Cap-M Model
    # --------------------------------------------------------------------------


    # Capitalization of earnings business valuation
    # Mostly for real estate
    def compute_value__cap_rate_market_model(self,
        industry_multiples,  # Dictionary of industry multiples
        market_cap,
        capitalization_rate  # net operating income / value
        ):
        npv = np.nan
        return npv / capitalization_rate


    # --------------------------------------------------------------------------
    # Market Relative Model
    # --------------------------------------------------------------------------
    
    def equity_value(
        market_value_of_equity,
        market_value_of_debt,
        cash
    ):
        return market_value_of_equity + market_value_of_debt - cash


    # Enterprise-Based Approach
    def compute_market_value(
            self,
            equity_value,
            expected_ebitda,
            ebitda):
        return (equity_value)/(ebitda) * expected_ebitda


    # def compute_value__relative_valuation_market_model(self,
    #     industry,
    #     ebitda
    #     ):
    #     return ebitda * self.__industry_multiples[industry]

    
    # --------------------------------------------------------------------------
    # DCF Model
    # Assuming the dividend doesnt grow: price = (DIV_1)/(1+R) + (DIV_2)/(1+R)...
    # Assuming dividend is expected to grow: price = (DIV)/(R-g)
    # --------------------------------------------------------------------------
    

    def compute_cost_of_equity(
        risk_free_rate,
        market_rate_of_return,
        beta
    ):
        return risk_free_rate + beta * (market_rate_of_return - risk_free_rate)


    def compute_wacc(cost_of_equity):

        value_of_equity = np.nan
        equity = np.nan
        debt = np.nan
        cost_of_debt = np.nan
        corporate_tax_rate = np.nan

        wacc = (cost_of_equity) * ( (value_of_equity) / (equity + debt) )
        wacc += (debt / (equity + debt)) * cost_of_debt * (1 - corporate_tax_rate)
        return wacc


    # Discount cashflow model
    def compute_value__dcf(self,
        ebitda_projection,  # 5-year projection # TODO use a MA
        wacc,  # Discount rate r == wacc
        # cashflow_multiple,
        ):
        
        year_count = len(ebitda_projection)
        npv = 0
        for y in range(0, year_count):
            ebitda = ebitda_projection[y]
            npv += ebitda / (1 + wacc) ** (y+1)
        
        return npv
