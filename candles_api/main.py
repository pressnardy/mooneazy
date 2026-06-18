from candles_api.api import get_candles


def main():
    supported_symbols = {
        'crypto': {'BTCUSDT', 'ETHUSDT'}
    }
    parameters = {
        'symbol': 'BTCUSDT', 'interval': '15m', 'limit': 100
    }
    print(get_candles(parameters=parameters, supported_symbols=supported_symbols))

if __name__ == "__main__":
    main()
