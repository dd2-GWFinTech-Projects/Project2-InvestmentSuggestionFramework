

class PortfolioBuilder:

    def __init__(self, debug_level=0):
        self.debug_level = debug_level

    def build_suggested_portfolio(self, customer_metrics, stock_score_lists):
        """
        Construct a suggested portfolio based on scores assigned to stocks through various analysis techniques.

        :param customer_metrics: CustomerMetrics instance containing high-level portfolio design requirements from the customer.
        :param stock_score_lists: List-of-lists containing stocks with associated score.
        :return:
        """
