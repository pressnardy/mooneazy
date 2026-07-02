from ultimate_setups import signals
from ultimate_setups.config import ULTIMATE_SCALPING_SETTINGS as scalping_configs
from candles_api import api


class Setups:
    def __init__(self, 
            symbol:str = 'BTCUSDT', 
            configs:dict = scalping_configs, 
            get_candles:callable = api.get_candles, 
            get_signals:callable = signals.get_signals
        ):
        self._configs = configs
        self._symbol = symbol
        self._get_candles = get_candles
        self._get_signals = get_signals
        self._htf1_candles = self.get_candles(parameters=self._configs['htf1_parameters'])
        self._htf2_candles = self.get_candles(parameters=self._configs['htf2_parameters'])
        self._trading_candles = self.get_candles(parameters=self._configs['trading_tf_parameters'])

    def get_candles(self, parameters):
        # print(parameters)
        parameters['symbol'] = self._symbol
        return self._get_candles(parameters=parameters)

    def get_trade_signals(self):
        configs = self._configs
        
        signals = self._get_signals(
            htf1_candles=self._htf1_candles,
            htf2_candles=self._htf2_candles,
            tranding_candles=self._trading_candles,
            pivot_lookback=configs['pivot_lookback'],
            fo_lookback=configs['fo_lookback'],
            ema_cross_periods=configs['ema_cross_periods'],
            interval=configs['trading_tf_parameters']['interval'],
            tp_rrrs=configs['tp_rrrs'],
        )
        return signals
    

def get_signals(
        supported_symbols: list = scalping_configs['supported_symbols']
    )->list[dict]:
    all_signals = []
    for symbol in supported_symbols:
        signals = Setups(symbol=symbol).get_trade_signals()
        all_signals.append(signals)
    
    return all_signals



