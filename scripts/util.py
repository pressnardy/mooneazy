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
    parameter:
        signal_time (unix_time): the timestamp to check.
        uptime_duration (int): duration in minutes.
    """
    uptime_duration_in_seconds = get_interval_in_seconds(interval)
    current_time = datetime.now(timezone.utc).timestamp()
    difference = abs(current_time - signal_time / 1000)

    return difference <= uptime_duration_in_seconds
