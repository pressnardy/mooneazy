import copy
from datetime import datetime, timezone
from pullback_strategy import config


def is_significant_pullback(
    impulse, pullback, min_fib_retracement, max_fib_retracement
    ):
    # print(f'util called: impulse: {impulse}, trend impulse{pullback}')
    # make sure pullback and impulse are in opposite directions

    if impulse: 
        retracement = pullback / impulse
        if float(retracement) < 0.0:
            # print(f'form util{retracement}')
            return max_fib_retracement >= abs(retracement) >= min_fib_retracement
    return False


def combine_pivots(resistance_pivots, support_pivots):
    cleaned_highs = [
        {'time': i['time'], 'value': i['high']} for i in resistance_pivots
    ]
    cleaned_lows = [
        {'time': i['time'], 'value': i['low']} for i in support_pivots
    ]

    all_pivots = cleaned_highs + cleaned_lows
    ordered_pivots = sorted(all_pivots, key=lambda x: x['time'])
    return ordered_pivots


def eliminate_triggers(triggers):
    """
    prevents subsequent candles that share a lookback high from 
    triggering sell signal for the same level before the previous 
    signal is stopped out the trade
    """
    level_triggers = copy.deepcopy(triggers)
    for i in level_triggers:
        i_time = i["trigger_candle"]["time"]
        for j in level_triggers:
            j_time = j["trigger_candle"]["time"]
            if i["level"] == j["level"] and i_time < j_time:
                i_lookback_hl = i["lookback_hl"]
                j_lookback_hl = j["lookback_hl"]
                if "sell" in i["signal_type"] and i_lookback_hl >= j_lookback_hl or \
                        "buy" in i["signal_type"] and i_lookback_hl <= j_lookback_hl:
                    level_triggers = [t for t in level_triggers if t != j]

    return level_triggers

def get_interval_in_seconds(interval):
    interval_value = int(interval[:1])
    time_symbol = interval[-1].lower()
    interval_in_seconds = 0
    if time_symbol == 'm':
        interval_in_seconds = interval_value * 60
    if time_symbol == 'h':
        interval_in_seconds = interval_value * 3600
    if time_symbol == 'd':
        interval_in_seconds = interval_value * 3600 * 24
    if time_symbol == 'w':
        interval_in_seconds = interval_value * 3600 * 24 * 7
    return interval_in_seconds


def is_active_signal(signal_time, interval):
    """
    Check if the signal trigger time is within the last uptime duration.
    parameter:
        signal_time (unix_time): the timestamp to check.
        uptime_duration (int): duration in minutes.
    """
    uptime_duration_in_seconds = get_interval_in_seconds(interval)
    current_time = datetime.now(timezone.utc).timestamp()
    difference = abs(current_time - signal_time / 1000)

    return difference <= uptime_duration_in_seconds


def is_tested(candles, level, signal_type, max_breach=4):
    breach = 0
    
    for candle in candles:
        if int(candle["time"]) < int(level["time"]):
            continue
        level_value = level["value"]
        if candle["close"] < level_value and "buy" in signal_type:
            breach += 1
        if candle["close"] > level_value and "sell" in signal_type:
            breach += 1
        if breach >= max_breach:
            return True
    return False


