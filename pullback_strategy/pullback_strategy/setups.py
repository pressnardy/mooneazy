from candles_api import api
from pullback_strategy import signals
from pullback_strategy import config

def get_setup_signal(symbol):
    HTF_INTERVAL, HTF_LIMIT = config.HTF_ARGS
    TRADING_TF_INTERVAL, TRADING_TF_LIMIT = config.TRADE_TF_ARGS
    EMA_PERIODS = config.EMA_PERIODS
    LOOKBACK_VALUES = config.LOOKBACK_VALUES

    htf_params = {'symbol': symbol,'interval': HTF_INTERVAL, 'limit': HTF_LIMIT}
    trading_tf_parameters = {
        'symbol': symbol,'interval': TRADING_TF_INTERVAL, 'limit': TRADING_TF_LIMIT
    }
    htf_candles = api.get_candles(htf_params)
    trading_candles = api.get_candles(trading_tf_parameters)

    trade_signals = signals.get_trade_signals(
        htf_candles=htf_candles,
        trading_candles=trading_candles,
        trading_interval=TRADING_TF_INTERVAL,
        ema_periods=EMA_PERIODS,
        lookback_values=LOOKBACK_VALUES[:-1],
        fo_lookback=LOOKBACK_VALUES[-1]
    )
    return trade_signals


def get_setup_signals(symbols:list = []):
    if not symbols:
        symbols = config.SUPPORTED_SYMBOLS
    signals = []
    for symbol in symbols:
        signals.extend(get_setup_signal(symbol))
    return signals or None

    





