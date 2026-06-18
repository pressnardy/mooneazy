from candles_api import api
from pullback_strategy import signals as pullback_signals
from range_strategy import signals as range_signals
from breakout_strategy import signals as breakout_signals
from scripts.config import ConfigParser


class Analyze:
    def __init__(self, symbol, config_parser):
        self.symbol = symbol
        self.config = config_parser
        self.htf1_candles = self.get_candles('4h', 200)
        self.htf2_candles = self.get_candles('1d', 200)
        self.m30_candles = self.get_candles('30m', 200)
        self.m15_candles = self.get_candles('m15', 100)
        self.tp_rrrs = self.config.tp_rrrs
        self.sl_padding = self.config.sl_padding

    def get_candles(self, interval, limit):
        parameters = {
            'symbol': self.symbol,
            'interval': interval,
            'limit': limit
        }
        return api.get_candles(pamameters=parameters)
    
    def get_pullpack_signal(self):
        config = self.config.pullback_settings
        signals = pullback_signals.get_trade_signals(
            htf_candles = self.htf1_candles,
            trading_candles = self.m15_candles,
            trading_interval = '15m',
            lookback_values = config.lookback_values,
            fo_lookback = config.fo_lookback,
            tp_rrrs = self.tp_rrrs,
            sl_padding = self.sl_padding
        )
        return signals
    
    def get_breakout_signal(self):
        signals = []
        configs = self.config.breakout_configs   
        breakout_parameters = {
            'htf1_candles': self.htf1_candles,
            'htf2_candles': self.htf2_candles,
            'lookback_left': configs.lookback_left,
            'min_opposite_candles': configs.minimum_opposite_candles,
            'ema_cross_periods': configs.ema_cross_periods,
            'hull_period': configs.hull_period,
            'tp_rrrs': self.tp_rrrs,
            'sl_padding': self.sl_padding
        }
        m15_params = breakout_parameters.update({
            'interval': '15m', 'trading_candles': self.m15_candles
        })
        m30_params = breakout_parameters.update({
            'interval': '30m', 'trading_candles': self.m30_candles
        })
        m15_signal = breakout_signals.get_signal(**m15_params)
        m30_signal = breakout_signals.get_signal(**m30_params)

        if m15_signal:
            signals.extend(m15_signal)
        if m30_signal:
            signals.extend(m30_signal)
        return signals 

    def get_range_signal(self):
        config = self.config.range_configs
        signals = range_signals.get_trade_signal(
            trade_tf_candles=self.m30_candles, 
            htf1_candles=self.htf1_candles, 
            htf2_candles=self.htf2_candles, 
            pivot_lookback=self.config.pi, 
            fo_lookback=config.fo_lookback, 
            ema_cross_periods=self.config.ema_cross_periods,
            tp_rrrs=self.tp_rrrs,
            sl_padding=self.sl_padding,
            interval='30m'
        )
        return signals 
    
    def get_signals(self):
        signals = []
        if breakout_signal := self.get_breakout_signal():
            signals.extend(breakout_signal)
        if range_signal := self.get_breakout_signal():
            signals.extend(range_signal)
        if pullback_signals := self.get_breakout_signal():
            signals.extend(pullback_signals)
        return signals


def get_signals(supported_symbols, config_parser):
    signals = []
    for symbol in supported_symbols:
        if symbol_signals := Analyze(symbol, config_parser).get_signals():
            signals.extend(symbol_signals)