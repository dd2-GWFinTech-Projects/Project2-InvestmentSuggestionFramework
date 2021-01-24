from main.valuation.ValuationCalculator import ValuationCalculator
from unittest import TestCase
from main.datastructures.IntegrationTestHelper import IntegrationTestHelper

class TestValuationCalculator(TestCase):

    def test_valuation_calculator_analyze(self):

        valuation_calculator = ValuationCalculator()
        test_helper = IntegrationTestHelper()
        stock_info_container = test_helper.build_container_financial_metadata()
        stock_info_container = test_helper.build_container_price_history(stock_info_container)
        valuation_calculator.analyze(stock_info_container)

        all_tickers = stock_info_container.get_all_tickers()
        self.assertEqual(3, all_tickers)

        all_financial_metadata = stock_info_container.get_all_financial_metadata()

        # self.assertTrue(score_appl.get_score() != 0)
        # self.assertTrue(score_tsla.get_score() != 0)
        # self.assertTrue(score_msft.get_score() != 0)
        # self.assertEqual("PriceForecasting.ARMA", score_appl.get_analysis_source())
        # self.assertEqual("PriceForecasting.ARMA", score_tsla.get_analysis_source())
        # self.assertEqual("PriceForecasting.ARMA", score_msft.get_analysis_source())


    # def test_compute_value__dcf(self):
    #     valuation_calculator = ValuationCalculator()
    #     npv_actual = valuation_calculator.compute_value__dcf(
    #         ebitda_projection=[-645000.00, 189430.00, 183115.00, 187266.00, 191375.00, 195432.00, 199427.00,
    #                            203348.00, 207184.00, 210923.00, 214550.00],
    #         wacc=0.08)
    #     npv_expected = 621178.98
    #     self.assertAlmostEqual(npv_expected, npv_actual, 1)


    # def test_compute_value_list(self):
    #     self.fail()

