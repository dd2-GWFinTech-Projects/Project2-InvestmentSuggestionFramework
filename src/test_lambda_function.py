from unittest import TestCase
from lambda_function import *

def test_get_recommended_portfolio():

    class Test(TestCase):

        def test_get_recommended_portfolio(self):
            portfolio_actual = get_recommended_portfolio("Long", 5000, "Medium", "Intermediate")
            portfolio_expected = "AAPL (100) - BNGO (100) - CIIC (100)"
            self.assertEqual(portfolio_expected, portfolio_actual)
