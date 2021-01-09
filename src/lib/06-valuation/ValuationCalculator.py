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


    # TODO Correlate industries to changing dividends
    def compute_value__dividend_discount_model(self,
        ticker,
        dividend_yield_fractional, # Dividend yield
        npv, # Net present value
        wacc, # Weighted cost of capital
        eps, # Earnings per share
        market_cap
    ):
        r = cost of equity capital
        g = growth rate
        npv = dividend_next_year / (r - g)
        return
    

    # Capitalization of earnings business valuation
    # Mostly for real estate
    def compute_value__market_model_1(self,
        industry_multiples,  # Dictionary of industry multiples
        market_cap,
        capitalization_rate  # net operating income / value
        ):
        return npv / capitalization_rate


    def compute_value__market_model_2(self,
        industry,
        industry_multiples,  # Dictionary of industry multiples
        ebitda
        ):
        return ebitda * multiple


    # Discount cashflow model
    def compute_value__dcf(self,
        ebitda_projection,
        r,  # Discount rate
        cashflow_multiple,
        ):
        
        for y in year_count:
            dcf = cashflow / (1 + r)
        
        return cashflow_forecast - future_loss_discount
