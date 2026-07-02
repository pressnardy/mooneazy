from ultimate_setups.strategies.ultimate_setups import UltimateSetups
from ultimate_setups.core.indicators import EmaCross
from ultimate_setups.core.trading import get_trade


def get_signals(
        htf1_candles, 
        htf2_candles, 
        tranding_candles,
        pivot_lookback, 
        fo_lookback, 
        ema_cross_periods, 
        interval, 
        tp_rrrs
    ):
    fast_ema_period, slow_ema_period = ema_cross_periods
    htf1_trend = 'buy' if EmaCross(
        candles=htf1_candles, 
        fast_ema_period=fast_ema_period,
        slow_ema_period=slow_ema_period
    ).is_bullish() else 'sell'
    htf2_trend = 'buy' if  EmaCross(
        candles=htf2_candles, 
        fast_ema_period=fast_ema_period,
        slow_ema_period=slow_ema_period
    ).is_bullish() else 'sell'
    ult_setups = UltimateSetups(
        candles=tranding_candles,
        fo_lookback=fo_lookback,
        pivot_lookback=pivot_lookback
    )
    signals = ult_setups.get_in_trend_signals(htf1_trend, htf2_trend)
    if not signals:
        return None
    trade_signals = []
    tp1_rrr, tp2_rrr = tp_rrrs
    for signal in signals:
        signal['interval'] = interval
        trade_signals.append(get_trade(
            signal=signal, tp1_rrr=tp1_rrr, tp2_rrr=tp2_rrr
        ))
    return signals or None
    

