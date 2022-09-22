import math

import backtrader as bt

from backtrader.indicators import Highest
from backtrader.indicators import Lowest

from matplotlib.pyplot import subplot

import symbol_data

class DonchianChannel(bt.Indicator):

    lines = (
        'basis', 
        'high', 'low',
        'high_volume', 'low_volume'
    )
    params = (
        ('period', 21),
    )

    plotinfo = dict(
        # Add extra margins above and below the 1s and -1s
        # plotymargin=0.15,

        # Plot a reference horizontal line at 1.0 and -1.0
        # plothlines=[0, 1, 2, 3],

        # Simplify the y scale to 1.0 and -1.0
        # plotyticks=[1.0, -1.0],

        subplot=False,
    )

    plotlines = dict(
        high_volume=dict(_plotskip=True,), 
        low_volume=dict(_plotskip=True,),
    )

    def __init__(self):
        
        self.l.high     = Highest(self.data.high, period=self.p.period)
        self.l.low      = Lowest(self.data.low, period=self.p.period)
        self.l.basis    = (self.l.high + self.l.low) / 2

        self.l.high_volume  = Highest(self.data.volume, period=self.p.period)
        self.l.low_volume   = Lowest(self.data.volume, period=self.p.period)
