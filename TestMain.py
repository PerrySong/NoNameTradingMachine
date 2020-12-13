from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
mode_path = os.path.dirname(os.path.abspath(sys.argv[0]))

from strategies.TestStrategy import TestStrategy
from datetime import datetime
import backtrader as bt


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