from Binance import Binance
from Evaluator import Evaluator
from Strategies import Strategies
from Trading import Trading
import json
from decimal import Decimal, getcontext
import sys

# sequentially backtest all strategies
def backtest_strategies(symbols = [], interval = '4h', plot = False, evaluators = [],
                       options = dict(starting_balance = 100, initial_profits = 1.01, initial_stop_loss = 0.9,
                        incremental_profits = 1.005, incremental_stop_loss = 0.995)):
    coins_tested = 0
    trade_value = options['starting_balance']

    for symbol in symbols:
        print(symbol)
        model = Trading(symbol = symbol, timeframe = interval)

        for ev in evaluators:
            resulting_balance = ev.backtest(
                model,
                starting_balance = options['starting_balance'],
                initial_profits = options['initial_profits'],
                initial_stop_loss = options['initial_stop_loss'],
                incremental_profits = options['incremental_profits'],
                incremental_stop_loss = options['incremental_stop_loss']
            )

            # display the results of a strategy matching on a symbol
            if resulting_balance != trade_value:
                print(ev.strategy.__name__ + ": Starting balance: " + str(trade_value) + ": Resulting_balance: " + str(round(resulting_balance, 2)))

                if plot:
                    model.plot_data(
                        buy_signals = ev.results[model.symbol]['buy_times'],
                        sell_signals = ev.results[model.symbol]['sell_times'],
                        title = ev.strategy.__name__ + " on " + model.symbol
                    )

                ev.profits_list.append(resulting_balance - trade_value)
                ev.update_result(trade_value, resulting_balance)

            coins_tested = coins_tested + 1

    for ev in evaluators:
        print("")
        ev.print_results()

STRATEGY_MATCH = "\n Strategy match!\nEnter 'b' to perform backtest\nEnter anything else to continue..."

# sequentially evaluate each strategy on each symbol
def evaluate_strategies(symbols = [], evaluators = [], interval = '1h',
                       options = dict(starting_balance = 100, initial_profits = 1.01, initial_stop_loss = 0.9,
                        incremental_profits = 1.005, incremental_stop_loss = 0.995)):
    matches = False
    for symbol in symbols:
        print(symbol, flush = True)
        model = Trading(symbol = symbol, timeframe = interval)
        for ev in evaluators:
            if ev.evaluate(model):
                matches = True
                print("\n" + ev.strategy.__name__ + " matched on " + symbol)
                print(STRATEGY_MATCH)
                user_in = input().lower()

                if user_in =='b':
                    resulting_balance = ev.backtest(
                        model,
                        starting_balance = options['starting_balance'],
                        initial_profits = options['initial_profits'],
                        initial_stop_loss = options['initial_stop_loss'],
                        incremental_profits = options['incremental_profits'],
                        incremental_stop_loss = options['incremental_stop_loss'],
                    )
                    model.plot_data(
                        buy_signals = ev.results[model.symbol]['buy_times'],
                        sell_signals = ev.results[model.symbol]['sell_times'],
                        title = ev.strategy.__name__ + " on " + symbol
                    )
                    print(ev.results[model.symbol])
                    user_in = input().lower()

    if not matches:
        print("No matches.", flush=True)

QUOTE_PROMPT="Select a quote asset: Enter '1' for BTC, '2' for BUSD, or '3' for USDT"
MAIN_PROMPT = "\nEnter 'b' to backtest all strategies on all symbols and summarize results\nEnter 'e' to execute strategies and prompt to backtest on matches\nEnter 'quit' to quit."

def main():
    print("Starting...")
    exchange = Binance()

    evaluators = [
        Evaluator(strategy = Strategies.boll_strategy),
        Evaluator(strategy = Strategies.ma_strategy),
        Evaluator(strategy = Strategies.ichimoku_bullish)
    ]

    print(QUOTE_PROMPT)
    user_in = input().lower()
    while user_in not in ['1', '2', '3', 'quit']:
        print("\nInvalid entry.")
        print(QUOTE_PROMPT)
        user_in = input().lower()
    if user_in == '1':
        print("Selected BTC.\n")
        quote = "BTC"
    elif user_in == '2':
        print("Selected BUSD.\n")
        quote = "BUSD"
    elif user_in == '3':
        print("Selected USDT.\n")
        quote = "USDT"
    elif user_in == 'quit':
        sys.exit(0)

    symbols = exchange.get_trading_symbols(quote_assets=[quote])

    print(MAIN_PROMPT)
    user_in = input().lower()
    while user_in not in ['b', 'e', 'quit']:
        print("\nInvalid entry.")
        print(MAIN_PROMPT)
        user_in = input().lower()

    if user_in == 'e':
        print("Evaluating...", flush = True)
        evaluate_strategies(symbols = symbols, interval = '5m', evaluators = evaluators)
    elif user_in == 'b':
        print("Backtesting...", flush = True)
        backtest_strategies(symbols = symbols, interval = '5m', plot = True, evaluators = evaluators)
    elif user_in == 'quit':
        sys.exit(0)

if __name__ == '__main__':
    main()