class ValuationCalculator:


    def __init__(self, debug_level):
        self.debug_level = 0
        # self.industry_multiples = {
        #     Industry
        #     EBITDA Average Multiple
        #     Healthcare information and technology
        #     24.81
        #     Airlines
        #     8.16
        #     Drugs, biotechnology
        #     13.29
        #     Hotels and casinos
        #     12.74
        #     Retail, general
        #     12.21
        #     Retail, food
        #     8.93
        #     Utilities, excluding water
        #     14.13
        #     Homebuilding
        #     10.95
        #     Medical equipment and supplies
        #     22.67
        #     Oil and gas, exploration and production
        #     4.89
        #     Telecom, equipment (phones & handheld devices)
        #     13.42
        #     Professional information services (big data)
        #     26.35
        #     Software, system & application
        #     24.00
        #     Wireless telecommunications services
        #     6.64
        # }
    

    def compute_value(self,
        industry,
        ):
        if industry_info[industry].has_dividend:
            return compute_value__dividend_discount_model()
        else if industry_info[industry].use_dcf:
            return compute_value__dcf()
        else if industry_info[industry].use_cap_rate_market_model:  # Need cap rate; prefer real estate industry
            return compute_value__cap_rate_market_model
        else:
            return compute_value__relative_valuation_market_model()



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
        npv = dividend_next_year / (r - g)
        return npv


    # Capitalization of earnings business valuation
    # Mostly for real estate
    def compute_value__cap_rate_market_model(self,
        industry_multiples,  # Dictionary of industry multiples
        market_cap,
        capitalization_rate  # net operating income / value
        ):
        return npv / capitalization_rate


    def compute_value__relative_valuation_market_model(self,
        industry,
        ebitda
        ):
        return ebitda * self.industry_multiples[industry]


    # Discount cashflow model
    def compute_value__dcf(self,
        ebitda_projection,
        r,  # Discount rate
        cashflow_multiple,
        ):
        
        for y in year_count:
            dcf = cashflow / (1 + r)
        
        return cashflow_forecast - future_loss_discount
