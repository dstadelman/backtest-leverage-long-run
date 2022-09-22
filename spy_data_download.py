import os

import yfinance as yf

import symbol_data

data = yf.download(['SPY'], start="1970-01-01", end="2022-12-31")

symbol_data.spy_data_save(data)
