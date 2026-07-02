import time
import pprint
from scripts.analysis import get_signals
from alerts.sounds import play_alert
from ultimate_setups.ultimate_setups.core import util

ALERT_UPTIME = 90

def get_signal_or_error():
    signal = None
    error = None
    try:
        signal = get_signals()
    except Exception as e:
        error = e
    return signal, error
    

def get_trade_alert():
    trade_alerts = []
    signals, error = get_signal_or_error()

    if signals is not None:
        for signal in signals:
            if not signal:
                continue
            trade_time = signal["time"]
            if util.is_active_signal(trade_time, ALERT_UPTIME):
                trade_alerts.append(signal)
    if not trade_alerts:
        trade_alerts = None
    return trade_alerts, error


def print_alert(trade_alerts):
    for trade in trade_alerts:
        pprint.pprint(trade, indent=4, depth=2)


def play_alert():
    from alerts import sounds
    sounds.play_alert()


def scalper():
    while True:
        trade_alerts, error = get_trade_alert()
        if error:
            continue
        if trade_alerts:
            print_alert(trade_alerts)
            play_alert()
        time.sleep(600)


if __name__ == "__main__":
    print("Scalper running...")
    scalper()
