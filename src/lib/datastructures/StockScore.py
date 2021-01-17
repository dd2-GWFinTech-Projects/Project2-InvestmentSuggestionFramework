
class StockScore:

    def __init__(self, analysis_source, score):
        self.__analysis_source = analysis_source
        self.__score = score

    def get_analysis_source(self):
        return self.__analysis_source

    def get_score(self):
        return self.__score
