from unittest import TestCase
from lambda_function import *


class TestLambdaFunction(TestCase):

    def test_get_recommended_portfolio(self):
        portfolio_actual = get_recommended_portfolio("Long", 5000, "Medium", "Intermediate")
        self.assertIsNotNone(portfolio_actual)
        self.assertNotEqual("", portfolio_actual)
        # portfolio_expected = "AAPL (100) - BNGO (100) - CIIC (100)"
        # self.assertEqual(portfolio_expected, portfolio_actual)
