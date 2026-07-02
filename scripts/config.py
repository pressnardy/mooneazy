# supported symbols
SUPPORTED_SYMBOLS = ['btcusdt', 'ethusdt', 'gld']

# trading candles settings
PULLBACK_STRATEGY_PARAMETERS = ['15m', 100]
BREAKOUT_STRATEGY_INTERVALS = ['15m', '30m']
BREAKOUT_STRATEGY_LIMIT = 200
RANGE_TRADING_PARAMETERS = ['15m', 200]

# htf candles parameters
HTF1_CANDLES_PARAMETERS = ['4h', 500]
HTF2_CANDLES_PARAMETERS = ['1d', 500]

# lookback settings
FO_LOOKBACK = 5
RANGE_STRATEGY_PIVOT_LOOKBACK = 30
LR_LOOKBACK_VALUES = [10, 20]

# indicator settings
EMA_CROSS_PERIODS = [8, 20]
HULL_PERIOD = 55

# trading settings
TP1_RRR = 2
TP2_RRR = 5
SL_PADDING = 0.001


class Configs:
    def __init__(self):
        # supported symbols
        self.supported_symbols = ['BTCUSDT', 'ETHUSDT', 'XAUUSDT']

        # trading candles parameters
        self.pullback_strategy_parameters = ['15m', 500]
        self.breakout_strategy_intervals = ['15m', '30m']
        self.breakout_strategy_limit = 500
        self.ult_trading_parameters = ['30m', 500]

        # higher timeframe candles parameters
        self.htf1_parameters = ['4h', 500]
        self.htf2_parameters = ['1d', 500]

        # lookback settings
        self.fo_lookback = 5
        self.ult_pivot_lookback = 30
        self.pullback_lookback_values = [10, 20]
        self.breakout_lookback = 5
                
        # indicator settings
        self.ema_cross_periods = [8, 20]
        self.hull_period = 55

        # tp rrrs
        self.pullback_tp_rrrs = [2, 5]
        self.breakout_tp_rrrs = [2, 5]
        self.ult_tp_rrrs = [1.5, 3]
        self.sl_padding = 0.001

        # breakout settings
        self.min_opposite_candles = 2



