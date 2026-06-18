from ultimate_setups.core.charting import Chart
from ultimate_setups.core import fakeouts, util
from ultimate_setups.core import settings


class UltimateSetups:
    def __init__(
            self, candles, buy_levels=[], sell_levels=[], 
            pivot_lookback=30, fo_lookback=5, default_quantity=None
        ):
        self._candles = candles
        self._pivot_lookback = pivot_lookback
        self._sell_levels = sell_levels
        self._buy_levels = buy_levels
        self._fo_lookback = fo_lookback
        self._fo_candles = candles[-self._fo_lookback:]
        self._range_quantity = default_quantity or len(candles)
        self._chart = self.start_chart()

    def start_chart(self):
        return Chart.start_chart(self._candles, self._range_quantity, self._pivot_lookback)

    def buy_levels(self):
        if not self._buy_levels:
            self._buy_levels = self._chart.lows()
        return self._buy_levels

    def all_buy_levels(self):
        if self._buy_levels:
            return self._buy_levels
        return self._chart.all_lows()

    def sell_levels(self):
        if not self._sell_levels:
            self._sell_levels = self._chart.highs()
        return self._sell_levels

    def all_sell_levels(self):
        if not self._sell_levels:
            self._sell_levels = self._chart.all_highs()
        return self._sell_levels

    def get_signals(self):
        candles, fo_lookback = self._candles, self._fo_lookback
        buy_levels, sell_levels = self.buy_levels(), self.sell_levels()
        signals = fakeouts.get_all_signals(candles, buy_levels, sell_levels, fo_lookback)
        if signals:
            sorted_signals = sorted(signals, key=lambda x: x['trigger_candle']['time'], reverse=True)
            return sorted_signals[0]
        return None

    def get_all_signals(self):
        candles, fo_lookback = self._candles, self._fo_lookback
        buy_levels, sell_levels = self.all_buy_levels(), self.all_sell_levels()
        all_signals = fakeouts.get_all_signals(
            candles, buy_levels, sell_levels, fo_lookback
        )
        if all_signals:
            return all_signals
        return None
    

class DCASetups(UltimateSetups):
    def __init__(
        self, 
        candles, 
        pivot_lookback=settings.ULTIMATE_DCA_SETTINGS['pivot_lookback']
        ):
        super().__init__(candles, pivot_lookback=pivot_lookback)


class DCASignals(UltimateSetups):
    def __init__(self, candles, buy_levels):
        self._candles = candles
        self._buy_levels = buy_levels   

    def get_signals(self):
        candle = self._candles[-1]
        level = util.resolve_level(level)
        for level in self._buy_levels:
            if level >= candle['low']:
                return {
                    "trigger_candle": candle, 
                    "lookback_hl": candle['low'], 
                    "signal_type": "dca_buy", 
                    "level": level
                }
        return None

