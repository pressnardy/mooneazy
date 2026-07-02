import json
from breakout_strategy.setups import get_trade_signals


def main():
    trade_signals = get_trade_signals()
    print(json.dumps(trade_signals, indent=4))


if __name__ == '__main__':
    main()






