from unittest import TestCase
from ..priceanalysis.PriceForecaster import PriceForecaster
from ..datastructures.TestHelper import TestHelper


class TestPriceForecaster(TestCase):
    def __init__(self):
        super().__init__()
        self.test_helper = TestHelper()

    def test_analyze(self):
        
        price_forecaster = PriceForecaster()
        stock_score_container = self.test_helper.build_container()
        price_forecaster.analyze(stock_score_container)
        score_appl = stock_score_container.get_stock_scores("AAPL")
        score_tsla = stock_score_container.get_stock_scores("TSLA")
        score_bngo = stock_score_container.get_stock_scores("BNGO")

        self.assertTrue(score_appl.get_score() > 0)
        self.assertTrue(score_tsla.get_score() > 0)
        self.assertTrue(score_bngo.get_score() > 0)

        self.assertEqual("PriceForecasting", score_appl.get_analysis_source())
        self.assertEqual("PriceForecasting", score_tsla.get_analysis_source())
        self.assertEqual("PriceForecasting", score_bngo.get_analysis_source())
