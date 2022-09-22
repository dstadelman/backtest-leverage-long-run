import csv
from datetime import datetime

import backtrader as bt

from backtrader.indicators.bollinger import BollingerBands
from backtrader.indicators.mabase import MovAv

import matplotlib.pyplot as plt

from indicators.donchian_channel import DonchianChannel

import symbol_data

class DonchianChannelTestStrategy(bt.Strategy):

    params = ()

    def __init__(self):
        self.rs = DonchianChannel(self.datas[0])

    def next(self):
        if not self.position:
            # buy one to force a chart to display
            self.buy()

    def stop(self):
        pass

def test_donchian_channel():

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(DonchianChannelTestStrategy)

    data = symbol_data.spy_data_load()

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Run over everything
    cerebro.run()

    plt.rcParams["figure.figsize"] = (15.5,9)
    plt.rcParams["figure.dpi"] = 100

    # Plot the result
    cerebro.plot(style='candlestick')
