class StockFilter:


    def __init__(self, debug_level=0):
        self.__debug_level = debug_level


    def filter(self, stock_info_container, apply_whitelist=False, use_predefined_test_stock_list=False):
        # TODO Remove items with invalid financial data

        if apply_whitelist:
            whitelist = { "AAPL", "TSLA", "BNGO" }
            old_stock_ticker_list = stock_info_container.get_all_tickers().copy()

            for stock_ticker in old_stock_ticker_list:
                if not (stock_ticker in whitelist):
                    stock_info_container.remove_ticker(stock_ticker)

        elif use_predefined_test_stock_list:

            # TODO Implement use_predefined_test_stock_list
            # def get_tickers(self):
            #     return [ "LRN", "ZYXI", "LMNX", "PETS", "AUDC", "HMI", "CEO", "HUYA", "SNDR", "TDS", "EQC", "LNTH", "SHLX",
            #              "CAJ", "DOYU", "JNPR", "ORCC", "JNJ", "NVS", "CRSA", "TSCO", "STN", "CECE", "FLWS", "CERN", "SIMO",
            #              "XOM", "MTRN", "LHX", "ODFL", "SCPL", "MAA", "HUBG", "CASY", "TRV", "TDY", "LCII", "ACTG", "CMG",
            #              "HLI", "ECOM", "BMTC", "NOVT", "FLIR", "AVD", "WBK", "GLW", "NPTN", "MET", "KE", "FN", "ACLS", "IBOC",
            #              "WRI", "PRGS", "MGPI", "CFR", "TSEM", "PCRX", "BXS", "BHP", "FMBI", "MRVL", "ASML", "HTLF", "TFC",
            #              "ICHR", "SPXC", "BIG", "HEI", "BDGE", "FULT", "LORL", "COLB", "ACA", "VSH", "WSM", "SBNY", "SMTC",
            #              "BOKF", "CRUS", "ALAC", "GNSS", "MKSI", "OFG", "AMKR", "DIOD", "KLAC", "PFC", "MIXT", "PJT", "FFG",
            #              "UVSP", "FHB", "SFNC", "ITI", "SMSI", "TER", "RGEN", "AVAV", "RNST", "FORM", "FBMS", "APOG", "INMD",
            #              "AUB", "IEC", "VRNT", "ACIA", "AEIS", "ONTO", "UCTT", "OLED", "AMAT", "WIT", "RADA", "BMI", "KLIC",
            #              "HZO", "FFIC", "VMI", "RCII", "OMP", "FBP", "STL", "TSM", "ETH", "KTOS", "WBS", "MYRG", "LUNA", "MTZ",
            #              "ABCB", "BIDU", "CLFD", "ORN", "SIVB", "SYX", "DY", "HIMX", "VCEL", "DAR", "HVT", "TIGR", "UMC",
            #              "CTRN", "CELH", "MSTR" ]
            x=False

        return stock_info_container
