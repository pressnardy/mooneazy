from ultimate_setups.strategies.ultimate_setups import UltimateSetups
from range_strategy.htf_trend import is_bullish_cross
from range_strategy.trading import get_trade
from range_strategy.util import is_active_signal


def get_signal(
        trade_tf_candles, 
        htf1_candles, 
        htf2_candles, 
        pivot_lookback, 
        fo_lookback, 
        ema_cross_periods,
    ):
    fast_ema_period, slow_ema_period = ema_cross_periods
    valid_signals = []
    
    signals = UltimateSetups(
        candles = trade_tf_candles,
        pivot_lookback = pivot_lookback, 
        fo_lookback = fo_lookback,
    ).get_signals()

    is_bullish_htf1 = is_bullish_cross(htf1_candles,slow_ema_period, fast_ema_period)
    is_bullish_htf2 = is_bullish_cross(htf2_candles,slow_ema_period, fast_ema_period)

    if is_bullish_htf1 or is_bullish_htf2:
        buy_signals = [s for s in signals if 'buy' in s['signal_type']]
        valid_signals.extend(buy_signals)

    if not is_bullish_htf1 or not is_bullish_htf2:
        sell_signals = [s for s in signals if 'sell' in s['signal_type']]
        valid_signals.extend(sell_signals)
    
    return valid_signals or None


def get_trade_signal(
        trade_tf_candles, 
        htf1_candles, 
        htf2_candles, 
        pivot_lookback, 
        fo_lookback, 
        ema_cross_periods,
        tp_rrrs,
        sl_padding,
        interval
    ):
    tp1_rrr, tp2_rrr = tp_rrrs
    trade_signals = []
    signals = get_signal(
        trade_tf_candles, htf1_candles, htf2_candles, 
        pivot_lookback, fo_lookback, ema_cross_periods
    )
    
    if not signals:
        return None 
    for signal in signals:
        signal['interval'] = interval
        active_signal = is_active_signal(signal['breakout_candle']['time'], interval)
        trade_signal = get_trade(active_signal, tp1_rrr, tp2_rrr, sl_padding)
        if trade_signal:
            trade_signals.append(trade_signal)
    return trade_signals or None

    


