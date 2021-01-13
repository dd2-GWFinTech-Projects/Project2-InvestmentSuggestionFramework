from ..datastructures.StockScore import StockScore

class PortfolioBuilder:

    def __init__(self, debug_level=0):
        self.debug_level = debug_level
        self.weighting = { "Price": 0.5, "Valuation" 0.5 }

    def build_suggested_portfolio(self, customer_metrics, stock_score_container):
        """
        Construct a suggested portfolio based on scores assigned to stocks through various analysis techniques.

        :param customer_metrics: CustomerMetrics instance containing high-level portfolio design requirements from the customer.
        :param stock_score_container: StockScoreContainer containing stocks with associated score.
        :return:
        """

        portfolio_composite_scores = []
        for analysis_source in stock_score_container.stock_score_map.keys():

            w = self.weighting[analysis_source]

            # Accumulate raw scores across all analysis methods
            for stock_score in stock_score_container.stock_score_map[analysis_source]:
                ticker = stock_score.ticker
                raw_score = stock_score.score
                if not (ticker in portfolio_composite_scores):
                    portfolio_composite_scores[ticker] = StockScore(ticker, w * raw_score)
                else:
                    old_score = portfolio_composite_scores[ticker]
                    portfolio_composite_scores[ticker] = StockScore(ticker, w * raw_score + old_score.score)

        # Sort
        score_list = list(portfolio_composite_scores.values())
        def score_sort(stock_score):
            return stock_score.score
        sorted_score_list = score_list.sort(key=score_sort)
        return sorted_score_list