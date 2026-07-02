from pullback_strategy.pullback import get_valid_pullback_level
from pullback_strategy.fakeouts import get_active_signals
from pullback_strategy.trading import get_trade
from pullback_strategy import config


def get_trade_signal(
        trading_candles, 
        interval, 
        fo_lookback, 
        tp_rrrs, 
        sl_padding
    ):
    lookback_candles = trading_candles[-fo_lookback:]
    trigger_candle = trading_candles[-1]
    if trigger_candle['open'] > trigger_candle['close']:
        lookback_hl = min(c['low'] for c in lookback_candles)
    else:
        lookback_hl = max(c['high'] for c in lookback_candles)
    signal = {
        'trigger_candle': trigger_candle,
        'lookback_hl': lookback_hl,
        'interval': interval
    }
    trade_signal = get_trade(
        signal=signal, 
        tp1_rrr=tp_rrrs[0], 
        tp2_rrr=tp_rrrs[1], 
        sl_padding=sl_padding
    )
    return trade_signal


def get_trade_signals(
        htf_candles, 
        trading_candles, 
        trading_interval: str = '15min', 
        ema_periods: tuple = (8, 20), 
        lookback_values: tuple = (5, 5), 
        fo_lookback: int = 5
    ):
    trade_signals = []
    slow_ema, fast_ema = ema_periods
    lookback_left, lookback_right = lookback_values

    pullback_level = get_valid_pullback_level(
        htf_candles, trading_candles, slow_ema, fast_ema, 
        lookback_left, lookback_right
    )
    if not pullback_level:
        return None
    kwargs = {
        'candles': trading_candles, 
        'interval': trading_interval,
        'buy_levels': None,
        'sell_levels': None,
        'fo_lookback': fo_lookback,
    }

    if pullback_level['is_bullish'] == True:
        kwargs['buy_levels'] = pullback_level['pullback_pivot']
    if pullback_level['is_bullish'] == False:
        kwargs['sell_levels'] = pullback_level['pullback_pivot']

    active_signals = get_active_signals(**kwargs)
    for signal in active_signals:
        trade_signals.append(get_trade_signal(signal))

    return trade_signals

