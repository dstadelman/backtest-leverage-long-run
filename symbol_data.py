import os

import pandas as pd

import backtrader.feeds as btfeed

def spy_data_save(data):
    if not os.path.exists('data/'):
        os.makedirs('data/')
    data.to_csv('data/SPY.csv')


def spy_data_load():

    df = pd.read_csv('data/SPY.csv')

    df['Date'] = pd.to_datetime(df['Date'])

    # ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

    assert len(df.columns) == 7
    assert df.columns[0] == 'Date'
    assert df.columns[1] == 'Open'
    assert df.columns[2] == 'High'
    assert df.columns[3] == 'Low'
    assert df.columns[4] == 'Close'
    assert df.columns[6] == 'Volume'    


    return btfeed.PandasData(

        name='SPY',

        dataname=df,

        # dtformat=('%Y-%m-%d'),

        openinterest=  -1,

        datetime=       0,
        open=           1,
        high=           2,
        low=            3,
        close=          4,
        volume=         6,
    )
