#Importação
import backtrader as bt
import math

#Criando a classe da nossa estratégia
class strategy_rsi_bb(bt.Strategy):

    params = dict(
        stop_loss=0.1,  # price is 5% less than the entry point
        entryPrice = 0,
    )
        
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data, period=14)
        self.bb = bt.indicators.BollingerBands(self.data)


    def next(self):
        if self.rsi < 30 and self.data < self.bb.lines.bot:
            
            actualPrice = math.floor(self.data[0])
            #print("Good moment to buy. Buying at: ", actualPrice)
            actualCash = cerebro.broker.getcash()
            buysSize = (actualCash/actualPrice)
            self.buy()

            # stop_price = self.data.close[0] * (1.0 - self.p.stop_loss)
            # self.sell(exectype=bt.Order.Stop, price=stop_price)


            self.p.entryPrice = actualPrice;
            #print(self.p.entryPrice) 
            
        elif self.rsi > 70 and self.data > self.bb.lines.top:
            actualPrice = math.floor(self.data[0])
            #print("Good moment to sell. Selling at: ", actualPrice)

            actualCash = cerebro.broker.getcash()
            buysSize = (actualCash/actualPrice)
            self.sell()

        # if (self.p.entryPrice*(1-self.p.stop_loss) > self.data[0]) and self.position:
        #     print("StopLoss triggered! Lets sell.")
        #     print("EntryPoint", self.p.entryPrice)
        #     print("price", self.data*(1-self.p.stop_loss))
        #     self.close()




cerebro = bt.Cerebro()

#data = bt.feeds.GenericCSVData(dataname='2020_15minutes.csv',dtformat = 2)
data = bt.feeds.GenericCSVData(dataname='1.csv',dtformat = 2)

#data = bt.feeds.GenericCSVData(dataname='novo.csv',dtformat = 2,timeframe=bt.TimeFrame.Minutes,compression=15)
cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
cerebro.adddata(data)
cerebro.addstrategy(strategy_rsi_bb)
#cerebro.broker.setcash(1000000.0)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()

#cerebro.addsizer(backtrader.sizers.PercentSizer, percents=95)