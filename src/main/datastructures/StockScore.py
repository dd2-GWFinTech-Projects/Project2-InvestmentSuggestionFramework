
class StockScore:

    def __init__(self, ticker, analysis_source, score):
        self.__ticker = ticker
        self.__analysis_source = analysis_source
        self.__score = score

    def get_ticker(self):
        return self.__ticker

    def get_analysis_source(self):
        return self.__analysis_source

    def get_score(self):
        return self.__score
