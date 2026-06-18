from ultimatesetups.strategies import ultimate_setups as ult, trading
from ultimatesetups.core import apirequests, settings

SWING_SETTINGS = settings.ULTIMATE_SWING_SETTINGS
SCALPING_SETTINGS = settings.ULTIMATE_SCALPING_SETTINGS
DCA_SETTINGS = settings.ULTIMATE_DCA_SETTINGS

def get_wing_levels():
    swing_candles = apirequests.get_candles("4h", 500, "BTCUSDT")
    swing_setups = ult.SwingSetups(swing_candles, pivot_lookback=SWING_SETTINGS['pivot_lookback'])
    print("Swing Setups Buy Levels:", swing_setups.buy_levels())
    print("Swing Setups Sell Levels:", swing_setups.sell_levels())


def get_scalp_levels():
    candles = apirequests.get_candles("30m", 500, "BTCUSDT")
    setups = ult.SwingSetups(candles, pivot_lookback=SCALPING_SETTINGS['pivot_lookback'])
    print("scalp Setups Buy Levels:", setups.buy_levels())
    print("scalp Setups Sell Levels:", setups.sell_levels())


def get_dca_levels():
    candles = apirequests.get_candles("1d", 500, "BTCUSDT")
    setups = ult.SwingSetups(candles, pivot_lookback=DCA_SETTINGS['pivot_lookback'])
    print("dca Setups Buy Levels:", setups.buy_levels())
    print("dca Setups Sell Levels:", setups.sell_levels())


if __name__ == "__main__":
    get_scalp_levels() 