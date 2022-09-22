import csv
from datetime import date

import backtrader as bt
import backtrader.feeds as btfeed

import matplotlib.pyplot as plt

from indicators.supertrend import Supertrend

import symbol_data


class SuperTrendTestStrategy(bt.Strategy):
    params = ()

    def __init__(self):
        self.supertrend    = Supertrend(self.datas[0])

    def next(self):
        if not self.position:
            # buy one to force a chart to display
            self.buy()

    def stop(self):
        pass

def test_supertrend():

    data = symbol_data.spy_data_load()

    # check len probably failed
    assert data is not None

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(SuperTrendTestStrategy)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Run over everything
    cerebro.run()

    plt.rcParams["figure.figsize"] = (15.5,9)
    plt.rcParams["figure.dpi"] = 100

    # Plot the result
    cerebro.plot(style='candlestick')
