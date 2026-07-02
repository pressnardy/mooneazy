from ultimate_setups.core.charting import Chart
from ultimate_setups.core import fakeouts, util
from ultimate_setups.core import settings


class UltimateSetups:
    '''
    Generates buy levels and sell levels from candles.
    Accepts buy levels and sell levels
    Generates fakeout signals from buy levels and sell levels

    Parameters:
        candles: list of dicts of time and ohcl candles stick data
        buy_levels: list of dict of support pivot point with time and value
        sell_levels: list of dict of resistance pivot point with time and value
        pivot_lookback: the number of candles on both sides of a pivot
        fo_lookback: the number of candles considered for a fakeout
        default_quantity: number of candles analyzed to find the buy and sell levels
    '''
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
        return Chart.start_chart(
            self._candles, self._range_quantity, self._pivot_lookback
        )

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
        # print(f"from ult_setups get_signals {buy_levels}, {sell_levels}")
        signals = fakeouts.get_all_signals(candles, buy_levels, sell_levels, fo_lookback)
        # print(f"from ult_setups get_signals {signals}")
        if signals:
            sorted_signals = sorted(signals, key=lambda x: x['trigger_candle']['time'], reverse=True)
            return [sorted_signals[0]]
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
    
    def get_in_trend_signals(self, htf1_trend, htf2_trend):
        signals = self.get_signals()
        if not signals:
            return None
        print(f'in trend signals: {signals[-1]["signal_type"]}')
        buy_signals = [signal for signal in signals if 'buy' in signal['signal_type']]
        sell_signals = [signal for signal in signals if 'sell' in signal['signal_type']]
        trend_signals = []
        if htf1_trend == 'buy' or htf2_trend == 'buy':
            trend_signals.extend(buy_signals)
        if htf1_trend == 'sell' or htf2_trend == 'sell':
            trend_signals.extend(sell_signals)
        return trend_signals
        



