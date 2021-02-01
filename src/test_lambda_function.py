from unittest import TestCase
from lambda_function import *


class TestLambdaFunction(TestCase):

    def test_get_recommended_portfolio(self):
        portfolio_actual = get_recommended_portfolio("Long", 5000, "Medium", "Intermediate", use_test_data=True)
        print(portfolio_actual)
        self.assertIsNotNone(portfolio_actual)
        self.assertNotEqual("", portfolio_actual)
        portfolio_expected = "AAPL (100) - BNGO (100) - CIIC (100)"

        expected_portfolio_regex = r"AAPL \([0-9.-]+\) - TSLA \([0-9.-]+\) - MSFT \([0-9.-]+\)"
        self.assertRegex(actual_portfolio_str, expected_portfolio_regex)



        self.assertRegex Equal(portfolio_expected, portfolio_actual)
