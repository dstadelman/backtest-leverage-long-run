import datetime
import math
import sys

import backtrader as bt

from backtrader.observers import DrawDown

from backtrader.indicators.atr import AverageTrueRange
from backtrader.indicators import Highest
from backtrader.indicators import Lowest
from backtrader.indicators import MovingAverageSimple

import matplotlib.pyplot as plt

from indicators.donchian_channel import DonchianChannel
from indicators.supertrend import Supertrend


class LongTermSwing(bt.Strategy):

    params = (
        # other params here
    )

    def __init__(self):

        # To keep track of pending orders and buy price/commission
        self.order                  = None
        self.orderStop              = None

        self.last_trade             = None

        # entry
        self.ma200                  = MovingAverageSimple(self.datas[0],    period=200)

        self.dc                     = DonchianChannel(self.datas[0],        period=126)

        self.dc_long_loss_high      = 0
        self.dc_long_loss_low       = sys.maxsize
        self.dc_short_loss_high     = 0
        self.dc_short_loss_low      = sys.maxsize

        # exit
        self.protect_capital        = 5

        self.atr10                  = AverageTrueRange(self.datas[0], plot=False, period=10)


    def notify_order(self, order):

        if order.status in [order.Submitted]:
            return

        # assumes the instrument trading is in datas[0]
        # self.log_order(self.datas[0].datetime.date(0), self.datas[0].params.name, order)

        # order.Submitted:    'Submitted', 
        # order.Accepted:     'Accepted',
        # order.Partial:      'Partial',
        # order.Completed:    'Completed',
        # order.Rejected:     'Rejected',
        # order.Margin:       'Margin',
        # order.Cancelled:    'Cancelled',
        # order.Expired:      'Expired',

        if order.status not in [order.Submitted, order.Accepted, order.Partial]:
            self.order = None

        # reference code below

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        # if order.status in [order.Completed]:
        #     if order.isbuy():
        #         pass

            # else:  # Sell
            #     self.log_order('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
            #              (order.executed.price,
            #               order.executed.value,
            #               order.executed.comm))
                          
            # self.bar_executed = len(self)

        # elif order.status in [order.Canceled, order.Margin, order.Rejected]:
        #     self.log_order('Order Canceled/Margin/Rejected')


    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.last_trade     = trade


    def stop(self):

        # the system that is evaluating the entire strategy across all symbols 
        # will need to perform the action of 'closing' orders for the open
        # positions to calculate expectancy 

        pass


    def protect_capital_stop(self, price):

        if self.position.size > 0:
            atr_stop_price = self.position.price - (self.entry_atr * self.protect_capital)
            return price if price > atr_stop_price else atr_stop_price
        else:
            atr_stop_price = self.position.price + (self.entry_atr * self.protect_capital)
            return price if price < atr_stop_price else atr_stop_price


    def next(self):

        assert len(list(filter(lambda x: x.status == 2, self.broker.orders))) <= 2

        ###############################################################################################################
        # dc20 reset

        if self.last_trade is None or self.last_trade.pnl > 0:
            self.dc_long_loss_high      = 0
            self.dc_long_loss_low       = sys.maxsize
            self.dc_short_loss_high     = 0
            self.dc_short_loss_low      = sys.maxsize

        ###############################################################################################################
        # IN POSITION

        if self.position:

            self.dc_long_loss_high     = max(self.dc.l.high[0], self.dc_long_loss_high)
            self.dc_long_loss_low      = min(self.dc.l.low[0],  self.dc_long_loss_low)

            try:

                if self.position.size > 0:

                    if (    self.datas[0].close[ 0] < self.ma200[ 0]
                        and self.datas[0].close[-1] < self.ma200[-1]
                        and self.datas[0].close[-2] < self.ma200[-2]
                        and self.datas[0].close[-3] < self.ma200[-3]
                    ):
                        self.orderStop = self.sell(
                            # price=max(self.protect_capital_stop(self.orderStop.price), (self.dc.l.basis[0] + self.dc.l.low[0]) / 2), 
                            size=abs(self.position.size),
                            # exectype=bt.Order.Stop,
                            exectype=bt.Order.Market,
                            valid=bt.num2date(self.datas[0].datetime[1]))

                elif self.position.size < 0:

                    self.dc_short_loss_high     = max(self.dc.l.high[0], self.dc_short_loss_high)
                    self.dc_short_loss_low      = min(self.dc.l.low[0], self.dc_short_loss_low)

                    if (    self.datas[0].close[ 0] > self.ma200[ 0]
                        and self.datas[0].close[-1] > self.ma200[-1]
                        and self.datas[0].close[-2] > self.ma200[-2]
                        and self.datas[0].close[-3] > self.ma200[-3]
                    ):
                        self.orderStop = self.buy(
                            # price=min(self.protect_capital_stop(self.orderStop.price), (self.dc.l.basis[0] + self.dc.l.high[0]) / 2), 
                            size=abs(self.position.size),
                            # exectype=bt.Order.Stop,
                            exectype=bt.Order.Market,
                            valid=bt.num2date(self.datas[0].datetime[1]))

            except Exception as e:
                pass


        ###############################################################################################################
        # LONG ENTRY

        if  (       not self.position and self.order is None
            
                and self.datas[0].close[0] > 5                                          # close is over $5

                and self.datas[0].close[ 0] > self.ma200[ 0]
                and self.datas[0].close[-1] > self.ma200[-1]
                and self.datas[0].close[-2] > self.ma200[-2]
                and self.datas[0].close[-3] > self.ma200[-3]
                and self.datas[0].close[-4] > self.ma200[-4]

                and (   self.datas[0].close[0] > self.dc_long_loss_high
                    or  self.datas[0].close[0] < self.dc_long_loss_low
                    or  self.position
                )

        ):

            price_entry = self.datas[0].high[0]
            price_stop  = self.datas[0].close[0] - (self.atr10 * self.protect_capital)
            
            price_entry = round(price_entry, 2)
            price_stop  = round(price_stop, 2)

            price_entry = None

            self.dc_long_loss_high     = 0
            self.dc_long_loss_low      = sys.maxsize

            # sometimes self.datas[0].datetime[1] is not an index... 
            # but we need it to make an order
            try:

                if price_entry is not None:
                    self.order = self.buy(
                        size=int(1000 / (self.atr10 * self.protect_capital)),
                        price=price_entry,
                        exectype=bt.Order.Stop,
                        valid=bt.num2date(self.datas[0].datetime[1]),
                        transmit=False,
                    )
                else:
                    self.order = self.buy(
                        size=int(1000 / (self.atr10 * self.protect_capital)),
                        exectype=bt.Order.Market,
                        transmit=False,
                    )

                if self.order:

                    self.stop_price = price_stop
                    self.order_original_size = self.order.size

                    self.orderStop = self.sell(
                        price=price_stop, 
                        size=self.order.size, 
                        exectype=bt.Order.Stop,
                        valid=bt.num2date(self.datas[0].datetime[1]),
                        transmit=True,
                        parent=self.order)

            except Exception as e:
                print('WARNING: attempted to make order in %s on %s' % (self.datas[0].params.name, bt.num2date(self.datas[0].datetime[0])), file=sys.stderr)

        ###############################################################################################################
        # SHORT ENTRY

        if  (       not self.position and self.order is None
        
                and self.datas[0].close[0] > 5                                          # close is over $5

                and self.datas[0].close[ 0] < self.ma200[ 0]
                and self.datas[0].close[-1] < self.ma200[-1]
                and self.datas[0].close[-2] < self.ma200[-2]
                and self.datas[0].close[-3] < self.ma200[-3]
                and self.datas[0].close[-4] < self.ma200[-4]

                and (   self.datas[0].close[0] < self.dc_short_loss_low
                    or  self.datas[0].close[0] > self.dc_short_loss_high
                    or  self.position
                )
        ):

            price_stop  = self.datas[0].close[0] + (self.atr10 * self.protect_capital)
            price_entry = self.datas[0].low[0]

            price_entry = round(price_entry, 2)
            price_stop  = round(price_stop, 2)

            price_entry = None

            self.dc_short_loss_high     = 0
            self.dc_short_loss_low      = sys.maxsize

            # sometimes self.datas[0].datetime[1] is not an index... 
            # but we need it to make an order
            try:

                if price_entry is not None:
                    self.order = self.sell(
                        size=int(1000 / (self.atr10 * self.protect_capital)),
                        price=price_entry,
                        exectype=bt.Order.Stop,
                        valid=bt.num2date(self.datas[0].datetime[1]),
                        transmit=False,
                    )
                else:
                    self.order = self.sell(
                        size=int(1000 / (self.atr10 * self.protect_capital)),
                        exectype=bt.Order.Market,
                        transmit=False,
                    )

                if self.order:

                    self.stop_price = price_stop
                    self.order_original_size = self.order.size

                    self.orderStop = self.buy(
                        price=price_stop, 
                        size=self.order.size, 
                        exectype=bt.Order.Stop,
                        valid=bt.num2date(self.datas[0].datetime[1]),
                        transmit=True,
                        parent=self.order)

            except Exception as e:
                print('WARNING: attempted to make order in %s on %s' % (self.datas[0].params.name, bt.num2date(self.datas[0].datetime[0])), file=sys.stderr)
