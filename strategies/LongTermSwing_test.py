import datetime

import backtrader as bt

from backtrader.indicators.bollinger import BollingerBands
from backtrader.indicators.mabase import MovAv

import matplotlib.pyplot as plt

from strategies.LongTermSwing import LongTermSwing

import symbol_data


def test_LongTermSwing():

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(LongTermSwing)

    data = symbol_data.spy_data_load()

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Run over everything
    cerebro.run()

    plt.rcParams["figure.figsize"] = (15.5,9)
    plt.rcParams["figure.dpi"] = 100

    # Plot the result
    cerebro.plot(style='candlestick')

