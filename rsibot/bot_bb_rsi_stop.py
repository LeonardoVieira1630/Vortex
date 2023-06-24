# Importações
import websocket
import json
import pprint
import talib
import numpy
import config
from binance.client import Client
from binance.enums import *


# Constantes
SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_5m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
BB_PERIOD = 20
BB_STD_DEV = 2
TRADE_SYMBOL = 'BTCUSDT'
TRADE_QUANTITY = 0.001

# Armazena os preços de candles
closes = []
# Diz se o candle fechou ou não
in_position = False

# Cliente para comunicação com a Binance
client = Client(config.API_KEY, config.SECRET_KEY, tld='us')


# Função geral para enviar uma ordem de compra ou venda para a corretora
def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occurred - {}".format(e))
        return False

    return True


# Função para verificar se o candle atual está abaixo da banda inferior das Bollinger Bands
def is_candle_below_bb(close):
    if len(closes) >= BB_PERIOD:
        np_closes = numpy.array(closes[-BB_PERIOD:])
        upper, middle, lower = talib.BBANDS(np_closes, timeperiod=BB_PERIOD, nbdevup=BB_STD_DEV, nbdevdn=BB_STD_DEV)
        if close < lower[-1]:
            return True
    return False


# Função para verificar se o candle atual está acima da banda superior das Bollinger Bands
def is_candle_above_bb(close):
    if len(closes) >= BB_PERIOD:
        np_closes = numpy.array(closes[-BB_PERIOD:])
        upper, middle, lower = talib.BBANDS(np_closes, timeperiod=BB_PERIOD, nbdevup=BB_STD_DEV, nbdevdn=BB_STD_DEV)
        if close > upper[-1]:
            return True
    return False


# Callback de abertura da conexão websocket
def on_open(ws):
    print('opened connection')


# Callback de fechamento da conexão websocket
def on_close(ws):
    print('closed connection')


# Função que lida com a estratégia do RSI e o controle dos dados
def on_message(ws, message):
    global closes, in_position

    # Recebendo dados de candle da Binance
    print('received message')
    json_message = json.loads(message)
    # pprint.pprint(json_message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']
    pprint.pprint(candle)

    # Caso a mensagem recebida contenha o valor final do candle, entramos aqui
    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))  # Adicionando a informação ao array
        print("closes")
        print(closes)

        # Se já tivermos informações suficientes para o cálculo:
        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)

            print("all RSIs calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("the current RSI is {}".format(last_rsi))

            # Verifica se o mercado está sobre-comprado (RSI) e o candle atual está abaixo da banda inferior (BB)
            if last_rsi > RSI_OVERBOUGHT and is_candle_below_bb(float(close)):
                if in_position:
                    print("Overbought and below lower BB! Sell! Sell! Sell!")
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = False
                else:
                    print("It is overbought and below lower BB, but we don't own any. Nothing to do.")

            # Verifica se o mercado está sobre-vendido (RSI) e o candle atual está acima da banda superior (BB)
            if last_rsi < RSI_OVERSOLD and is_candle_above_bb(float(close)):
                if in_position:
                    print("It is oversold, but you already own it, nothing to do.")
                else:
                    print("Oversold and above upper BB! Buy! Buy! Buy!")
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = True


# Conexão via websocket com a Binance
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
