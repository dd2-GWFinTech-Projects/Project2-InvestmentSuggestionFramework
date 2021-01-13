from ..datastructures.StockInfo import StockInfo


class PortfolioBuilder:


    def __init__(self, debug_level=0):
        self.debug_level = debug_level
        self.weighting = { "Price": 0.5, "Valuation": 0.5 }


    def build_suggested_portfolio(self, customer_metrics, stock_score_container):
        """
        Construct a suggested portfolio based on scores assigned to stocks through various analysis techniques.

        :param customer_metrics: CustomerMetrics instance containing high-level portfolio design requirements from the customer.
        :param stock_score_container: StockInfoContainer containing stocks with associated score.
        :return:
        """

        # Compute composite score and sort
        stock_score_list = self.compute_composite_scores(customer_metrics, stock_score_container)
        stock_score_list = self.sort_stock_score_list(stock_score_list)

        # Compute number of shares
        stock_shares_list = self.compute_shares(customer_metrics, stock_score_list)

        # Transform to string representation
        return self.generate_recommendation_string(stock_shares_list)


    def compute_composite_scores(self, customer_metrics, stock_score_container):

        portfolio_composite_scores = {}
        for analysis_source in stock_score_container.stock_score_map.keys():

            w = self.weighting[analysis_source]

            # Accumulate raw scores across all analysis methods
            for stock_score in stock_score_container.stock_score_map[analysis_source]:
                ticker = stock_score.ticker
                raw_score = stock_score.score
                if not (ticker in portfolio_composite_scores):
                    portfolio_composite_scores[ticker] = StockInfo(ticker, w * raw_score)
                else:
                    old_score = portfolio_composite_scores[ticker]
                    portfolio_composite_scores[ticker] = StockInfo(ticker, w * raw_score + old_score.score)

        # Sort
        return list(portfolio_composite_scores.values())


    def sort_stock_score_list(self, score_list):
        def score_sort(stock_score):
            return stock_score.score
        score_list.sort(reverse=True, key=score_sort)
        return score_list


    def compute_shares(self, customer_metrics, stock_score_list):
        total_nbr_shares = 400 #customer_metrics.investmentAmount
        stock_shares_list = []
        for stock_score in stock_score_list:
            ticker = stock_score.ticker
            score = stock_score.score
            stock_shares_list.append(StockInfo(ticker, 100))
        return stock_shares_list


    def generate_recommendation_string(self, stock_shares_list):
        recommendation_string = ""
        i = 0
        for share_count in stock_shares_list:
            ticker = share_count.ticker
            nshares = share_count.score
            if i > 0:
                recommendation_string += " - "
            recommendation_string += f"{ticker} ({nshares})"
            i += 1

        return recommendation_string
