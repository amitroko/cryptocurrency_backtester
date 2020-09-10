from pyti.smoothed_moving_average import smoothed_moving_average as sma
from pyti.exponential_moving_average import exponential_moving_average as ema
from pyti.bollinger_bands import lower_bollinger_band as lbb
from pyti.bollinger_bands import upper_bollinger_band as ubb

def ichimoku_cloud(df):
    #Tenkan-sen aka conversion line
    nine_period_high = df['high'].rolling(window = 9).max()
    nine_period_low = df['low'].rolling(window = 9).min()
    df['tenkansen'] = (nine_period_high + nine_period_low) / 2

    #Kijun-sen aka base line
    period26_high = df['high'].rolling(window = 26).max()
    period26_low = df['low'].rolling(window = 26).min()
    df['kijunsen'] = (period26_high + period26_low) / 2

    #Senkou Span A aka leading span A
    df['senkou_a'] = ((df['tenkansen'] + df['kijunsen']) / 2).shift(26)

    #Senkou Span B aka leading span B
    period52_high = df['high'].rolling(window = 52).max()
    period52_low = df['low'].rolling(window = 52).min()
    df['senkou_b'] = ((period52_high + period52_low) / 2).shift(52)

    #Chikou Span aka most recent closing price
    df['chikouspan'] = df['close'].shift(-26)

    return df

class Indicators:
    indicators = {
        "sma": sma,
        "ema": ema,
        "lbb": lbb,
        "ubb": ubb,
        "ichimoku": ichimoku_cloud
    }

    @staticmethod
    def add_indicator(df, name, col_name, args):
        try:
            if name == "ichimoku":
                df = ichimoku_cloud(df)
            else:
                df[col_name] = Indicators.indicators[name](df['close'].tolist(), args)
        except Exception as e:
            print("Failed to compute " + name)
            print(e)