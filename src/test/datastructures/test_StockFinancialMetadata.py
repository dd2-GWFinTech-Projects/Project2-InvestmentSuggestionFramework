from unittest import TestCase
from main.lib.datastructures.StockFinancialMetadata import StockFinancialMetadata


class TestStockFinancialMetadata(TestCase):


    def test_combine_data_list_map(self):
        list_map_1 = self.__generate_data_list_map("AAPL", 0)
        list_map_2 = self.__generate_data_list_map("AAPL", 0)
        combined_list_map = list_map_1.combine_data_list_map(list_map_2)
        self.assertEqual(3, len(combined_list_map))
        self.assertEqual(3, len(combined_list_map[0]))


    def __generate_data_list_map(self, stock_ticker, offset):
        stock_financial_metadata_1 = StockFinancialMetadata(stock_ticker, [
            self.__generate_data_map("12/31/2018", offset+0, offset+0, offset+0),
            self.__generate_data_map("12/31/2019", offset+1, offset+1, offset+1),
            self.__generate_data_map("12/31/2020", offset+2, offset+2, offset+2)
        ])


    def __generate_data_map(self, date, field1, field2, field3):
        return {
            "date": date,
            "field1": field1,
            "field2": field2,
            "field3": field3
       }
