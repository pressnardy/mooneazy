import json
from breakout_strategy.setups import get_trade_signals
from breakout_strategy.breakout_strategy import htf_trend
from breakout_strategy.breakout_strategy import signals

def main():
    trade_signals = get_trade_signals()
    print(trade_signals)


if __name__ == '__main__':
    main()






