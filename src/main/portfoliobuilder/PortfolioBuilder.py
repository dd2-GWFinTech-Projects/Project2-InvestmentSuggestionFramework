

class PortfolioBuilder:


    def __init__(self, debug_level=0):
        self.__debug_level = debug_level
        self.__weighting = {"Price": 0.5, "Valuation": 0.5}


    # --------------------------------------------------------------------------
    # Portfolio building functions
    # --------------------------------------------------------------------------


    def build_suggested_portfolio(self, customer_metrics, stock_info_container):
        """
        Construct a suggested portfolio based on scores assigned to stocks through various analysis techniques.

        :param customer_metrics: CustomerMetrics instance containing high-level portfolio design requirements from the customer.
        :param stock_info_container: StockInfoContainer containing stocks with associated score.
        :return:
        """

        # Compute composite score and sort
        stock_score_list = self.__compute_composite_scores(customer_metrics, stock_info_container)
        stock_score_list = self.__sort_stock_score_list(stock_score_list)

        # Compute number of shares
        stock_shares_list = self.__compute_shares(customer_metrics, stock_score_list)
        return stock_shares_list
        # Transform to string representation


    def add_hedge_positions(self, stock_info_container):
        # TODO
        return stock_info_container


    def transform_suggested_portfolio_str(self, portfolio):
        recommendation_string = ""
        i = 0
        for share_count in portfolio:
            ticker = share_count.ticker
            nshares = share_count.score
            if i > 0:
                recommendation_string += " - "
            recommendation_string += f"{ticker} ({nshares})"
            i += 1

        return recommendation_string


    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------


    def __compute_composite_scores(self, customer_metrics, stock_info_container):

        # Ticker -> Composite Score dictionary
        portfolio_composite_scores = {}

        # Number of raw scores used to compute composite
        portfolio_composite_score_counts = {}

        # Sum the weighted scores
        for stock_score in stock_info_container.get_all_scores_single_level():

            stock_ticker = stock_score.get_ticker()
            score = stock_score.get_score()
            analysis_source = stock_score.get_analysis_source()
            w = self.__weighting[analysis_source]

            # Initialize dictionaries
            if not (stock_ticker in portfolio_composite_scores):
                portfolio_composite_scores[stock_ticker] = 0
            if not (stock_ticker in portfolio_composite_score_counts):
                portfolio_composite_score_counts[stock_ticker] = 0

            # Add scores
            portfolio_composite_scores[stock_ticker] += w * score
            portfolio_composite_score_counts[stock_ticker] += 1

        # Average over the number of analysis methods
        for stock_ticker in portfolio_composite_scores.keys():
            portfolio_composite_scores[stock_ticker] /= portfolio_composite_score_counts[stock_ticker]

        return list(portfolio_composite_scores.values())


    def __sort_stock_score_list(self, score_list):
        def score_sort(stock_score):
            return stock_score.get_score()
        score_list.sort(reverse=True, key=score_sort)
        return score_list


    def __compute_shares(self, customer_metrics, stock_score_list):

        total_nbr_shares = 400  #customer_metrics.investmentAmount

        # Compute total score
        total_score = 0.0
        for stock_score in stock_score_list:
            total_score += stock_score.get_score()

        # Scale shares proportionally   #TODO this is wrong bc it does not take money into account
        portfolio = {}
        for stock_score in stock_score_list:
            num_shares = total_nbr_shares * stock_score.get_score() / total_score
            portfolio[stock_score.get_ticker()] = num_shares

        return portfolio
