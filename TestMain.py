from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
mode_path = os.path.dirname(os.path.abspath(sys.argv[0]))
# sys.path.append(mode_path + "/strategies")
# sys.path.append(mode_path + "/indicators")
from strategies.TestStrategy import TestStrategy
from datetime import datetime
import backtrader as bt

# Create a Stratey
# class TestStrategy(bt.Strategy):
#
#     def log(self, txt, dt=None):
#         ''' Logging function fot this strategies'''
#         dt = dt or self.datas[0].datetime.date(0)
#         print('%s, %s' % (dt.isoformat(), txt))
#
#     def __init__(self):
#         # Keep a reference to the "close" line in the data[0] dataseries
#         self.dataclose = self.datas[0].close
#
#         # To keep track of pending orders
#         self.order = None
#
#     def notify_order(self, order):
#         if order.status in [order.Submitted, order.Accepted]:
#             # Buy/Sell order submitted/accepted to/by broker - Nothing to do
#             return
#
#         # Check if an order has been completed
#         # Attention: broker could reject order if not enough cash
#         if order.status in [order.Completed]:
#             if order.isbuy():
#                 self.log('BUY EXECUTED, %.2f' % order.executed.price)
#             elif order.issell():
#                 self.log('SELL EXECUTED, %.2f' % order.executed.price)
#
#             self.bar_executed = len(self)
#
#         elif order.status in [order.Canceled, order.Margin, order.Rejected]:
#             self.log('Order Canceled/Margin/Rejected')
#
#         # Write down: no pending order
#         self.order = None
#
#     def next(self):
#         # Simply log the closing price of the series from the reference
#         self.log('Close, %.2f' % self.dataclose[0])
#
#         # Check if an order is pending ... if yes, we cannot send a 2nd one
#         if self.order:
#             return
#
#         # Check if we are in the market
#         if not self.position:
#
#             # Not yet ... we MIGHT BUY if ...
#             if self.dataclose[0] < self.dataclose[-1]:
#                     # current close less than previous close
#
#                     if self.dataclose[-1] < self.dataclose[-2]:
#                         # previous close less than the previous close
#
#                         # BUY, BUY, BUY!!! (with default parameters)
#                         self.log('BUY CREATE, %.2f' % self.dataclose[0])
#
#                         # Keep track of the created order to avoid a 2nd order
#                         self.order = self.buy()
#
#         else:
#
#             # Already in the market ... we might sell
#             if len(self) >= (self.bar_executed + 5):
#                 # SELL, SELL, SELL!!! (with all possible default parameters)
#                 self.log('SELL CREATE, %.2f' % self.dataclose[0])
#
#                 # Keep track of the created order to av

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    # Add a strategies
    # cerebro.addstrategy(bt.strategies.MA_CrossOver, fast=5, slow=15)
    cerebro.addstrategy(TestStrategy)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10) # https://www.backtrader.com/docu/sizers/sizers/

    cerebro.broker.set_cash(100_000)
    # Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.001)
    # Datas are in a subfolder of the samples. Need to find where the script is
        # because it could have been called from anywhere
    datapath = os.path.join(mode_path, './data/oracle.csv')
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime(2000, 1, 1),
        todate=datetime(2000, 12, 31),
        reversed=False
    )
    cerebro.adddata(data)
    print('Starting portfolio value: %.2f' % cerebro.broker.get_value())
    cerebro.run()
    print('Final portfolio value: %.2f' % cerebro.broker.get_value())
    cerebro.plot()