import pandas as pd
import requests
import json
from plotly.offline import plot
import plotly.graph_objs as go
from Binance import Binance

class Trading:
    def __init__(self, symbol, timeframe:str = '4h'):
        self.symbol = symbol
        self.timeframe = timeframe
        self.exchange = Binance()
        self.df = self.exchange.get_symbol_data(symbol, timeframe)
        self.last_price = self.df['close'][len(self.df['close']) - 1]

    # plot price data of symbol with additional analysis specified by parameters
    def plot_data(self, buy_signals = False, sell_signals = False, title:str = "", indicators = []):
        df = self.df

        candle = go.Candlestick(
            x = df['time'],
            open = df['open'],
            close = df['close'],
            high = df['high'],
            low = df['low'],
            name = "Candlesticks"
        )

        data = [candle]

        if df.__contains__('fast_sma'):
            fsma = go.Scatter(
                x = df['time'],
                y = df['fast_sma'],
                name = "Fast SMA",
                line = dict(color = ('rgba(0, 204, 204, 50)'))
            )
            data.append(fsma)

        if df.__contains__('slow_sma'):
            ssma = go.Scatter(
                x = df['time'],
                y = df['slow_sma'],
                name = "Slow SMA",
                line = dict(color = ('rgba(0, 102, 204, 50)'))
            )
            data.append(ssma)

        if df.__contains__('low_boll'):
            lowbb = go.Scatter(
                x = df['time'],
                y = df['low_boll'],
                name = "Low Bollinger Band",
                line = dict(color = ('rgba(153, 51, 255, 50)'))
            )
            data.append(lowbb)

        if df.__contains__('tenkansen'):
            tksn = go.Scatter(
                x=df['time'],
                y=df['tenkansen'],
                name = "Tenkansen",
                line = dict(color = ('rgba(25, 28, 0, 50)'))
            )
            data.append(tksn)

        if df.__contains__('kijunsen'):
            kjsn = go.Scatter(
                x = df['time'],
                y = df['kijunsen'],
                name = "Kijunsen",
                line = dict(color = ('rgba(153, 76, 0, 50)'))
            )
            data.append(kjsn)

        if df.__contains__('senkou_a'):
            snka = go.Scatter(
                x=df['time'],
                y=df['senkou_a'],
                name = "Senkou A",
                line = dict(color = ('rgba(255, 255, 0, 50)'))
            )
            data.append(snka)

        if df.__contains__('senkou_b'):
            snkb = go.Scatter(
                x = df['time'],
                y = df['senkou_b'],
                name = "Senkou B",
                fill = "tonexty",
                line = dict(color = ('rgba(153, 153, 0, 50)'))
            )
            data.append(snkb)

        if buy_signals:
            buys = go.Scatter(
                x = [item[0] for item in buy_signals],
                y = [item[1] for item in buy_signals],
                name = "Buy Signals",
                mode = "markers",
                marker_size = 20)
            data.append(buys)

        if sell_signals:
            sells = go.Scatter(
                x = [item[0] for item in sell_signals],
                y = [item[1] for item in sell_signals],
                name = "Sell Signals",
                mode = "markers",
                marker_size = 20)
            data.append(sells)

        layout = go.Layout(
            title = title,
            xaxis = {
                "title": self.symbol,
                "rangeslider": {"visible": False},
                "type": "date"
            },
            yaxis = {
                "fixedrange": False,
            }
        )
        fig = go.Figure(data = data, layout = layout)

        plot(fig, filename = 'data/' + title + '.html')