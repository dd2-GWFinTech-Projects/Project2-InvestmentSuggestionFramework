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
        return npv / capitalization_rate


    # --------------------------------------------------------------------------
    # Market Relative Model
    # --------------------------------------------------------------------------


    def compute_value__relative_valuation_market_model(self,
        industry,
        ebitda
        ):
        return ebitda * self.industry_multiples[industry]

    
    # --------------------------------------------------------------------------
    # DCF Model
    # --------------------------------------------------------------------------
    

    def compute_cost_of_equity(
        risk_free_rate,
        market_rate_of_return,
        beta
    ):
        return risk_free_rate + beta * (market_rate_of_return - risk_free_rate)


    def compute_wacc(cost_of_equity):
        wacc = (cost_of_equity) * ( (value_of_equity) / (equity + debt) )
        wacc += (debt / (equity + debt)) * cost_of_debt * (1 - corporate_tax_rate)
        return wacc


    # Discount cashflow model
    def compute_value__dcf(self,
        ebitda_projection,  # 5-year projection
        wacc,  # Discount rate r == wacc
        # cashflow_multiple,
        ):
        
        year_count = len(ebitda_projection)
        for y in range(0, year_count):
            ebitda = ebitda_projection[y]
            npv += ebitda / (1 + r)
        
        return npv

    def test__compute_value__dcf():
        npv_actual = compute_value__dcf(
            ebitda_projection = [ -645000.00, 189430.00, 183115.00, 187266.00, 191375.00, 195432.00, 199427.00, 203348.00, 207184.00, 210923.00, 214550.00 ],
            wacc=0.08)
        npv_expected = 621178.98 

