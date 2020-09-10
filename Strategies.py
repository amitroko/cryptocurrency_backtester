from Indicators import Indicators

class Strategies:

    @staticmethod
    def ma_strategy(df, i: int):
        if not df.__contains__('slow_sma'):
            Indicators.add_indicator(df, name = "sma", col_name = "slow_sma", args = 30)

        buy_price = 0.96 * df['slow_sma'][i]
        if buy_price >= df['close'][i]:
            return min(buy_price, df['high'][i])

        return False


    @staticmethod
    def boll_strategy(df, i:int):
        if not df.__contains__('low_boll'):
            Indicators.add_indicator(df, name = "lbb", col_name = "low_boll", args = 14)

        buy_price = 0.975 * df['low_boll'][i]
        if buy_price >= df['close'][i]:
            return min(buy_price, df['high'][i])

        return False

    @staticmethod
    def ichimoku_bullish(df, i: int):
        if not df.__contains__('tenkansen') or not df.__contains__('kijunsen') or \
                not df.__contains__('senkou_a') or not df.__contains__('senkou_b'):
            Indicators.add_indicator(df, name = "ichimoku", col_name = None, args = None)

        if i - 1 > 0 and i < len(df):
            if df['senkou_a'][i] is not None and df['senkou_b'][i] is not None:
                if df['tenkansen'][i] is not None and df['tenkansen'][i - 1] is not None:
                    if df['close'][i - 1] < df['tenkansen'][i - 1] and \
                            df['close'][i] > df['tenkansen'][i] and \
                            df['close'][i] > df['senkou_a'][i] and \
                            df['close'][i] > df['senkou_b'][i]:
                                return df['close'][i]

        return False

