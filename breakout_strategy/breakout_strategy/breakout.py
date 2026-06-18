
def is_bullish(candle):
    return candle['close'] > candle['low']


def is_valid_min_oposite(lookback_candles, breakout_candle, min_oposit=None):
    if not min_oposit:
        min_oposit = len(lookback_candles) / 3
    count_bearish = 0
    count_bullish = 0
    for candle in lookback_candles:
        if is_bullish(candle):
            count_bullish += 1
        if not is_bullish(candle):
            count_bearish += 1
    if is_bullish(breakout_candle) and count_bearish >= min_oposit:
        return True
    if not is_bullish(breakout_candle) and count_bullish >= min_oposit:
        return True
    return False


def is_engulfing_breakout(lookback_candles, breakout_candle, min_opposit):
    max_high = max(candle['high'] for candle in lookback_candles)
    min_low = min(candle['low'] for candle in lookback_candles)
    mid_range = (max_high - min_low) / 2 + min_low
    
    if not is_valid_min_oposite(lookback_candles, breakout_candle, min_opposit):
        return False
    if is_bullish(breakout_candle):
        return breakout_candle['low'] < mid_range and breakout_candle['close'] > max_high
    return breakout_candle['high'] > mid_range and breakout_candle['close'] < min_low

def breaks_level(candle, level):
    if is_bullish(candle):
        return candle['close'] > level > candle['low']
    return candle['close'] < level < candle['high']
    

def breaks_emas(breakout_candle, fast_ema_value, slow_ema_value):
    return breaks_level(
        breakout_candle, fast_ema_value
    ) and breaks_level(breakout_candle, slow_ema_value)

def touches(candle, value):
    return candle['high'] > value > candle['low']


def is_tight_hull(candles, hull_55_values):
    hull_dict = {}
    for i, hull in enumerate(hull_55_values):
        hull_dict[hull] = candles[i]

    count_touches = 0
    for hull, candle in hull_dict.items():
        if touches(candle, hull):
            count_touches += 1
    if count_touches > len(candles) / 2:
        return True
    
def is_cross(candle, fast_ema_values, slow_ema_values):
    fast_ema_value = fast_ema_values[-1]
    prev_fast_ema_value = fast_ema_values[-2]
    slow_ema_value = slow_ema_values[-1]
    prev_slow_ema_value = slow_ema_values[-2]

    if not breaks_emas(candle, fast_ema_value, slow_ema_value):
        return False
    if is_bullish(candle):
        if fast_ema_value > slow_ema_value and (
            prev_fast_ema_value <= prev_slow_ema_value
            ):
            return True

    return  fast_ema_value < slow_ema_value and (
        prev_fast_ema_value >= prev_slow_ema_value
        )  
    

class BreakOut:
    def __init__(
            self, breakout_candles, fast_ema_values, 
            slow_ema_values, hull_values, min_opposite_candles
        ):
        self.lookback_candles = breakout_candles[: -1],
        self.breakout_candle = breakout_candles[-1],
        self.min_opposit = min_opposite_candles,
        self.fast_ema_values = fast_ema_values,
        self.slow_ema_values = slow_ema_values,
        self.hull_values = hull_values,
        
        self.score = self.calculate_score()

    def calculate_score(self):
        if is_engulfing_breakout(
            self.lookback_candles, 
            self.breakout_candle, 
            self.min_opposit
            ):
            score += 5
        if breaks_emas(
            self.breakout_candle, 
            self.fast_ema_values[-1], 
            self.slow_ema_values[-1]
            ):
            score += 2
        if is_tight_hull(
            self.lookback_candles, 
            self.breakout_candle, 
            self.hull_values
            ):
            score += 2
        if is_cross(
            self.breakout_candle, 
            self.fast_ema_values[-1], 
            self.fast_ema_values[-2], 
            self.slow_ema_values[-1], 
            self.slow_ema_values[-2]
            ):
            score += 1
        return score

    def is_valid(self, min_score=5):
        return self.score > min_score
    