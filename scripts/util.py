from datetime import datetime, timezone

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
    Multiplies the interval by 2 to ensure the signal stays valid throughout the next candle.
    parameter:
        signal_time (unix_time): the trigger candle start time i.e time.
        uptime_duration (int): duration in minutes.
    """
    # multiply by 2 to account for the time it takes for the candle to close and the signal to be generated
    uptime_duration_in_seconds = get_interval_in_seconds(interval) * 2
    current_time = datetime.now(timezone.utc).timestamp()
    difference = abs(current_time - signal_time / 1000)

    return difference <= uptime_duration_in_seconds

