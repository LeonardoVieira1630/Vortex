#Importação
import backtrader as bt
import math

#Criando a classe da nossa estratégia
class strategy_rsi_bb(bt.Strategy):

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data, period=14)
        self.bb = bt.indicators.BollingerBands(self.data)


    def next(self):
        if self.rsi < 30 and self.data < self.bb.lines.bot:#and self.bb: 
            
            #print(cerebro.broker.getvalue())
            actualPrice = math.floor(self.data[0])
            print("buy at: ", actualPrice)
            actualCash = cerebro.broker.getcash()
            #print(actualCash)
            buysSize = (actualCash/actualPrice)
            #print(buysSize)
            #self.buy(size=round(buysSize, 4))#Quantidade de tokens
            self.buy()#Quantidade de tokens
            #self.sell(exectype=bt.Order.StopTrail, trailpercent=0.02)
        
        if self.rsi > 70 and self.data > self.bb.lines.top:
            actualPrice = math.floor(self.data[0])
            print("sell at: ", actualPrice)

            # actualCash = cerebro.broker.getcash()
            # selsSize = (actualCash/actualPrice)/4
            # print(selsSize)
            self.close()



cerebro = bt.Cerebro()

#data = bt.feeds.GenericCSVData(dataname='daily.csv',dtformat = 2)
data = bt.feeds.GenericCSVData(dataname='novo.csv',dtformat = 2,timeframe=bt.TimeFrame.Minutes,compression=15)
cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
cerebro.adddata(data)
cerebro.addstrategy(strategy_rsi_bb)
#cerebro.broker.setcash(1000000.0)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()

#cerebro.addsizer(backtrader.sizers.PercentSizer, percents=95)