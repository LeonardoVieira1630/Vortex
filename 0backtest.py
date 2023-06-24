"""
    O backtest.pt roda uma simulação de como a estratégia do rsi performaria em
um determinado periodo de tempo.
    Essa biblioteca é fenomenal para testes antes de realmente colocarmos
dinheiro na aplicação. 
"""
#Importação
import backtrader as bt

#Criando a classe da nossa estratégia
class RSIStrategy(bt.Strategy):

    def __init__(self):
       self.rsi = bt.indicators.RSI(self.data, period=14)

    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=0.1)#Quantidade da moeda
        
        if self.rsi > 70 and self.position:
            self.close()



cerebro = bt.Cerebro()

#data = bt.feeds.GenericCSVData(dataname='daily.csv',dtformat = 2)
#data = bt.feeds.GenericCSVData(dataname='novo.csv',dtformat = 2,timeframe=bt.TimeFrame.Minutes,compression=15)

#março ate jun = 4% lucro
data = bt.feeds.GenericCSVData(dataname='1.csv', dtformat=2, timeframe=bt.TimeFrame.Days)

cerebro.adddata(data)
cerebro.addstrategy(RSIStrategy)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()




# import backtrader as bt
# import numpy as np

# class MyStrategy (bt.Strategy):

#     #Parametros de los indicadores
#     params = (('BBandsperiod', 20),('devfactor',2), ('RSIperiod',14))

#     def log(self, txt, dt=None):
#         ''' Logging function for this strategy'''
#         dt = dt or self.datas[0].datetime.date(0)
#         #print('%s, %s' % (dt.isoformat(), txt))


#     def __init__(self):
#         #keep a reference to the close
#         self.dataclose = self.datas[0].close
        
#         #add a BBand and RSI
#         self.rsi=bt.indicators.RSI_SMA(period=self.p.RSIperiod,plotname='mysma')
#         self.bband = bt.indicators.BollingerBands(period=self.p.BBandsperiod, devfactor=self.p.devfactor)

#     def next(self):
        
#             if self.rsi[0] < 30:
#                 self.log('BUY CREATE, %.2f' % self.dataclose[0])
#                 self.buy()
     
#             if self.rsi[0] >70:
#                 self.log('SELL CREATE, %.2f' % self.dataclose[0])
#                 self.sell()



# cerebro = bt.Cerebro()
# data = bt.feeds.GenericCSVData(dataname='novo.csv',dtformat = 2,timeframe=bt.TimeFrame.Minutes,compression=15)
# cerebro.adddata(data)

# cerebro.addstrategy(MyStrategy)


# cerebro.run()
# cerebro.plot()
