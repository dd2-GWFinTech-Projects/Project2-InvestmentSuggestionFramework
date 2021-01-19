from unittest import TestCase
from ..priceanalysis.PriceForecaster import PriceForecaster
from ..datastructures.TestHelper import TestHelper


class TestPriceForecaster(TestCase):
    def test_analyze(self):

        price_forecaster = PriceForecaster()
        test_helper = TestHelper()
        stock_info_container = test_helper.build_container_price_history()
        price_forecaster.analyze(stock_info_container)

        score_appl = stock_info_container.get_stock_scores("AAPL")
        score_tsla = stock_info_container.get_stock_scores("TSLA")
        score_msft = stock_info_container.get_stock_scores("MSFT")

        self.assertTrue(score_appl.get_score() > 0)
        self.assertTrue(score_tsla.get_score() > 0)
        self.assertTrue(score_msft.get_score() > 0)

        self.assertEqual("PriceForecasting", score_appl.get_analysis_source())
        self.assertEqual("PriceForecasting", score_tsla.get_analysis_source())
        self.assertEqual("PriceForecasting", score_msft.get_analysis_source())
