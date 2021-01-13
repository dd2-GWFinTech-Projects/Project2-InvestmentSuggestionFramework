# Contributors: Adam
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from time import time
import re
import matplotlib
import matplotlib.pyplot as plt
import random
import statsmodels.api as sm

class PortfolioBuilder2:

    def __init__(self, dataframe, investment_amount, risk, n_stocks, dev=False):
        self.dataframe = dataframe.set_index("date")
        self.investment_amount = investment_amount
        self.n_stocks = n_stocks
        self.risk = risk
        self.dev = dev

        if self.investment_amount < 20:
            raise ValueError("In the beta version you must invest atleast  $20.")

        if self.n_stocks < 3:
            raise ValueError("I need you to want at least 3 stocks... Try again.")
        else:
            self.dataframe = self.dataframe.loc[
                             :, (self.dataframe.iloc[-1] < self.investment_amount)
                             ]


    def replace_nans(self):
        self.dataframe = self.dataframe.fillna(method="ffill")
        self.dataframe = self.dataframe.fillna(method="bfill")

        return self.dataframe


    def dissolve_correlation_matrix(self, corr_matrix):
        dataframe = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape)).astype(np.bool)
        )
        dataframe = dataframe.stack().reset_index()
        dataframe.columns = ["row", "column", "value"]

        return dataframe


    def generate_corr_groups(
            self, corr_matrix, positive_threhold=0.33, negative_threshold=-0.33
    ):
        pos_corrs = self.dissolve_correlation_matrix(
            corr_matrix[(corr_matrix >= positive_threhold) & (corr_matrix != 1)]
        )
        no_corrs = self.dissolve_correlation_matrix(
            corr_matrix[
                (corr_matrix < positive_threhold)
                & (corr_matrix > negative_threshold)
                & (corr_matrix != 1)
                ]
        )
        neg_corrs = self.dissolve_correlation_matrix(
            corr_matrix[(corr_matrix <= negative_threshold) & (corr_matrix != 1)]
        )

        return pos_corrs, no_corrs, neg_corrs


    def select_n_stocks(self):
        self.dataframe = self.replace_nans()

        stats_df = self.dataframe.describe()
        stds = stats_df.T["std"]

        low_third = np.quantile(stds, 0.25)
        high_third = np.quantile(stds, 0.75)

        if self.risk == "Low":
            possible_syms = stds[stds <= low_third].index.values
        elif self.risk == "Medium":
            possible_syms = stds[(stds > low_third) & (stds < high_third)].index.values
        elif self.risk == "High":
            possible_syms = stds[stds >= high_third].index.values

        if self.dev:
            print(f"Possible stock symbols \n {possible_syms} \n")

        self.possible_stock_symbols = possible_syms

        corr = self.dataframe.loc[:, possible_syms].corr()

        pos, non, neg = self.generate_corr_groups(corr)

        # pick random combos from each group

        remainder = self.n_stocks % 3

        n = int((self.n_stocks - remainder) / 3)

        if self.dev:
            print(f"{n} positive, non, and negative corr \n")
            print(f"Remainder of {remainder} \n")
        # TODO: handle when no combos exist in correlation group

        pos_combos = pos.sample(n=n)
        non_combos = non.sample(n=(n + remainder))
        neg_combos = neg.sample(n=n)

        if self.dev:
            print(f"Non-correlated combos \n {pos_combos} \n")

        stocks = pd.concat([pos_combos, non_combos, neg_combos], axis=0)

        self.stock_correlations = stocks.reset_index(drop=True)

        if self.dev:
            print(f"Stock correlations \n {stocks} \n")

        return self.dataframe.loc[:, set(stocks.row.tolist() + stocks.column.tolist())]


    def get_shares(self):
        total = 0
        lowest_total = np.inf
        search_time = 2
        possible = self.select_n_stocks().iloc[-1]
        possible = possible.repeat(self.n_stocks)
        n_choice = self.n_stocks
        n_stock_buy = 1

        while (
                total <= (self.investment_amount * 0.9) or total >= self.investment_amount
        ):
            tot_time = 0
            s = time()

            while (
                    total <= (self.investment_amount * 0.9)
                    or total >= self.investment_amount
            ) and tot_time <= search_time:
                cur_stocks = np.random.choice(possible, n_choice)
                cur_stock_syms = list(
                    set(possible[possible.isin(cur_stocks)].index.values)
                )

                total = cur_stocks.sum()
                tot_time = time() - s

                if total <= self.investment_amount * 0.9:
                    n_stock_buy = np.floor(self.investment_amount / total)
                    total = total * n_stock_buy

            n_choice -= 1

            if self.dev:
                money = "${:,.2f}".format(total)
                str_syms = re.sub("[^a-zA-Z\s\,]+", "", str(cur_stock_syms))
                print(f"{int(n_stock_buy)} share(s) of {str_syms} for {money}")

            if n_choice == 0:
                print("No stocks exist for less than your investment amount...")
                break

            self.selected_stocks = cur_stock_syms
            self.shares = n_stock_buy
            self.dataframe = self.dataframe[self.selected_stocks]

            return cur_stock_syms, n_stock_buy


    def basic_viz(self, selected_stocks):
        fig = go.Figure()

        # Add Traces
        for i, s in enumerate(selected_stocks):
            color = random.choice(list(matplotlib.colors.cnames.values()))
            fig.add_trace(
                go.Scatter(
                    x=list(self.dataframe.index),
                    y=list(self.dataframe[s]),
                    name=f"{s}",
                    line=dict(color=f"{color}"),
                )
            )

        # a list of dicts with keys label, method, args

        button_dict = {"active": 0, "buttons": []}

        for i in range(len(selected_stocks)):

            bool_list = [False] * len(selected_stocks)
            bool_list[i] = True
            bool_list = [{"visible": bool_list}]

            if i == 0:
                temp = {
                    "label": "All Stocks",
                    "method": "update",
                    "args": [{"visible": [True] * len(selected_stocks)}],
                }
                button_dict["buttons"].append(temp)
                temp = {
                    "label": selected_stocks[0],
                    "method": "update",
                    "args": bool_list,
                }
                button_dict["buttons"].append(temp)

            else:
                temp = {
                    "label": selected_stocks[i],
                    "method": "update",
                    "args": bool_list,
                }

                button_dict["buttons"].append(temp)

        fig.update_layout(updatemenus=[button_dict])

        # Set title
        prices = self.dataframe[self.selected_stocks].iloc[-1].round(2).tolist()
        portfolio_display = list(zip(self.selected_stocks, prices))
        fig.update_layout(title_text=f"Your Random Portfolio")
        fig.update_xaxes(rangeslider_visible=True)
        fig.show()
