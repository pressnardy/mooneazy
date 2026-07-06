import time
import pprint
import traceback
import json
from scripts.analysis import get_signals
from alerts.sounds import play_alert
from scripts import util

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
            # pprint.pprint(signal, indent=4)
            if util.is_active_signal(signal["time"], signal["interval"]):
                trade_alerts.append(signal)
    if not trade_alerts:
        trade_alerts = None
    return trade_alerts, error


def print_alert(trade_alerts):
    for trade in trade_alerts:
        print(json.dumps(trade, indent=4))


def play_alert():
    from alerts import sounds
    sounds.play_alert()


def scalper():
    while True:
        trade_alerts, error = get_trade_alert()
        if error:
            traceback.print_exc()
            play_alert()
            time.sleep(60)
            continue
        if trade_alerts:
            print_alert(trade_alerts)
            play_alert()
        time.sleep(600)

def scalper_debugger():
    while True:
        trade_alerts, error = get_trade_alert()
        if error:
            raise error
        if trade_alerts:
            print_alert(trade_alerts)
            play_alert()
        time.sleep(30)

if __name__ == "__main__":
    print("Scalper running...")
    scalper_debugger()
