# 写一个backtrader 回测
import backtrader as bt
import backtrader_plotting as bplot
import logging as lg
import os


class MyStrategy(bt.Strategy):
    name = 'MyStrategy'
    logger = lg.getLogger(name)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lg.basicConfig(filemode='a', 
                        filename=f'log_{self.name}.txt', 
                        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=lg.INFO)
        self.dataclose = self.datas[0].close


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        self.logger.info('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
    
    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
def get_data(*args, **kwargs):
    # Get data from the data feed
    data = bt.feeds.GenericCSVData(dataname=args[0],
                                    fromdate=args[1],
                                    todate=args[2],
                                    nullvalue=0.0,
                                    dtformat=('%Y-%m-%d'),
                                    datetime=0,
                                    high=1,
                                    low=2,)
    return data

data = get_data()
cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
cerebro.adddata(data)
cerebro.broker.setcash(100000)
cerebro.run()
