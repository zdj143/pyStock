from datetime import datetime, date, time
from datetime import timedelta
import pandas as pd
import numpy as np
import backtrader as bt
import backtrader_plotting as btplt
import sys
import os.path
import glob
from backtrader.feeds import PandasData


class PandasDataExtend(PandasData):
    # create new line
    lines = ('pe', 'roe', 'marketdays')
    params = (('pe', 15),
              ('roe', 16),
                ('marketdays', 30))

class StampDutyCommissionScheme(bt.CommissionScheme):
    """
    Stamp Duty Commission Scheme
    """
    params = (('stampduty', 0.0015),   # 印花税
              ('commission', 0.0005),    # 手续费
              ('stocklike', True),
              ('commtype', bt.Order.CommInfoBase.COMM_PERC),)

    def _getcommission(self, size, price, pseudoexec):
        """
        If size is greater than 0, this indicates a long/buy of share
        If size is less than 0, this indicates a short/sell of share

        Returns commission for a given transaction
        """
        if size > 0: # 买入 不计算印花税
            return size * price * self.p.commssion
        elif size < 0: # 卖出
            return size * price * (self.p.stampduty + self.p.commission)
        else:
            return 0.0

class Strategy(bt.Strategy):
    params = dict(
         rebal_monthday = [1],
         num_volume = 100,
         period = 5,
    )

    def log(self, txt, dt=None):
        """ Logging function fot this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

        # 上次交易股票的列表
        self.lastrank = []

        # 0号是指数不进入股票池，从1开始进入股票池
        self.stocks = self.datas[1:]

        # 记录以往的订单，在再平衡日要全部取消未完成的订单
        self.order.list = []

        # 移动平均线指标
        self.sma = {d:bt.ind.SMA(d, period=self.p.period) for d in self.datas}

        # 定时器
        self.add_timer(
            when=bt.Timer.SESSION_START,
            monthdays=self.p.rebal_monthday,
            monthcarry=True,   # 若再平衡日不是交易日，则顺延触发notify_timer
        )
    def notify_timer(self, timer, when, *args, **kwargs):
        if self.data0.datetime.date(0).month in [5, 9, 11]:
            self.rebalance_portfolio()  # 执行再平衡————调仓
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 接收到订单提交或者订单已经接收，这里不做处理
            return
        # 正常订单状

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('买单执行， %s, %.2f, %i' % (order.data._name, order.executed.price, order.executed.size))
            elif order.issell():
                self.log('卖单执行， %s, %.2f, %i' % (order.data._name, order.executed.price, order.executed.size))
        else:
            self.log('订单作废 %s， %s， isbusy=%i， size=%i， open price=%.2f' % (order.data._name, order.getstatusname(), order.isbusy, order.size, order.open_price))
