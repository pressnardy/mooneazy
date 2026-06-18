from ultimate_setups.core.settings import ULTIMATE_SCALPING_SETTINGS
from ultimate_setups.core.indicators import EmaCross
from ultimate_setups.core import apirequests


def get_crosses(period='1d', quantity=500, symbol='BTCUSDT'):
    """
    Get the ema cross trend for the scalping direction.
    """
    period = period or ULTIMATE_SCALPING_SETTINGS['trend']['period']
    quantity = quantity or ULTIMATE_SCALPING_SETTINGS['default_quantity']
    candles = apirequests.get_candles(period, quantity, symbol)
    fast_period = ULTIMATE_SCALPING_SETTINGS['trend']['fast_ema']
    slow_period = ULTIMATE_SCALPING_SETTINGS['trend']['slow_ema']
    
    crosses = EmaCross(
        candles, fast_ema_period=fast_period, slow_ema_period=slow_period
    ).get_crosses()
    return crosses or None


def get_trend_trades(crosses: list[dict], trades: list[dict]) -> list[dict]:
    """
    returns trades that match the trend direction of the crosses
    """
    trend_trades = []
    for trade in trades:
        # find the most recent cross before the trade
        cross = next((c for c in reversed(crosses) if c["time"] < trade["time"]), None)
        if cross and cross["direction"] == trade["direction"]:
            trend_trades.append(trade)
    return trend_trades or None


