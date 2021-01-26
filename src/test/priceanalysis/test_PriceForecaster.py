from unittest import TestCase
from main.priceanalysis.PriceForecaster import PriceForecaster
from test.lib.TestDataBuilder import TestDataBuilder


class TestPriceForecaster(TestCase):


    def test_price_forecaster_analyze(self):

        price_forecaster = PriceForecaster()
        test_data_builder = TestDataBuilder()
        stock_info_container = test_data_builder.build_container_price_history()
        price_forecaster.analyze(stock_info_container)

        score_aapl = stock_info_container.get_stock_score_list("AAPL")[0]
        score_bngo = stock_info_container.get_stock_score_list("BNGO")[0]
        score_ciic = stock_info_container.get_stock_score_list("CIIC")[0]

        self.assertTrue(score_aapl.get_score() != 0)
        self.assertTrue(score_bngo.get_score() != 0)
        self.assertTrue(score_ciic.get_score() != 0)

        self.assertEqual("PriceForecasting.ARMA", score_aapl.get_analysis_source())
        self.assertEqual("PriceForecasting.ARMA", score_bngo.get_analysis_source())
        self.assertEqual("PriceForecasting.ARMA", score_ciic.get_analysis_source())
