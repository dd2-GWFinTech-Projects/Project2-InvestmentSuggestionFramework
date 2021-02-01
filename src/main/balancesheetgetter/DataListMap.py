import numpy as np


class DataListMap:


    def __init__(self):
        self.__data_list_map = {}


    def combine(self, other):

        for stock_ticker in other.__data_list_map.keys():

            # Initialize empty list
            if not stock_ticker in self.__data_list_map:
                self.__data_list_map[stock_ticker] = []

            this_size = len(self.__data_list_map[stock_ticker])
            other_size = len(other.__data_list_map[stock_ticker])

            max_size = np.max(this_size, other_size)

            for i in range(0, max_size):
                other_data_map = other.__data_list_map[stock_ticker][i]

                # Shortcut for new list entry
                if i >= this_size:
                    self.__data_list_map[stock_ticker].append(other_data_map)
                    continue

                # Destructively combine the maps (TODO does not maintain data integrity)
                for key, value in other_data_map.items():
                    self.__data_list_map[stock_ticker][i][key] = value

        return self
