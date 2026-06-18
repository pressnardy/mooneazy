import json
import time
from urllib.request import Request, urlopen

# Fake error module simulation to ensure example runs; keep your local 'import api_errors'
try:
    import api_errors
except ImportError:
    class MockApiErrors:
        FailedToFetchCandles = Exception
    api_errors = MockApiErrors()


def get_start_time_end_time(period: str, quantity: int):
    end_time = int(time.time())
    
    # Base conversions to seconds
    if "m" in period:
        minutes = int(period.replace("m", ""))
        multiplier = minutes * 60
    elif "h" in period:
        hours = int(period.replace("h", ""))
        multiplier = hours * 60 * 60
    elif "d" in period:
        days = int(period.replace("d", ""))
        multiplier = days * 24 * 60 * 60
    else:
        multiplier = 24 * 60 * 60  # Default fallback to 1 day

    # Add a buffer (2x for daily to bypass weekends, 1.5x for intraday just in case)
    buffer_factor = 2 if "d" in period else 10
    total_seconds_back = int(quantity * multiplier * buffer_factor)
    
    start_time = end_time - total_seconds_back
    return start_time, end_time


def get_latest_candles(symbol: str, quantity: int, period: str) -> list:
    """Fetches historical candlestick data from Yahoo Finance without Pandas.

    Args:
        symbol: Ticker string (e.g., 'AAPL', 'BTC-USD').
        quantity: Exact number of latest candles to return.
        period: Time interval per candle ('1d', '1h', '15m', '1m').

    Returns:
        A list of dictionaries containing individual candle data.
    """
    start_time, end_time = get_start_time_end_time(period, quantity)
    
    # FIXED: Correct Yahoo Finance v8 API endpoint URL syntax
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={start_time}&period2={end_time}&interval={period}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    try:
        with urlopen(req) as response:
            raw_data = json.loads(response.read().decode())

        # Safely drill down into the JSON structure
        result = raw_data["chart"]["result"][0]
        timestamps = result.get("timestamp", [])
        quotes = result["indicators"]["quote"][0]

        # Extract native lists
        opens = quotes.get("open", [])
        highs = quotes.get("high", [])
        lows = quotes.get("low", [])
        closes = quotes.get("close", [])
        volumes = quotes.get("volume", [])

        candles = []
        # Defensive check against mismatched array lengths
        loop_limit = min(len(timestamps), len(opens), len(closes))

        for i in range(loop_limit):
            # Skip corrupted data points or empty market ticks
            if opens[i] is None or closes[i] is None:
                continue

            candles.append({
                "time": timestamps[i],
                "open": opens[i],
                "high": highs[i],
                "low": lows[i],
                "close": closes[i],
                "volume": volumes[i],
            })

        # Slice the list to return exactly the latest requested quantity
        return candles[-quantity:]
        
    except Exception as e:
        # 'from e' links the native error context to your custom API exception 
        raise api_errors.YahooFailedToFetchCandles(e.message)
        

if __name__ == "__main__":
    # Test with standard daily data
    candles = get_latest_candles(symbol="GLD", quantity=300, period="5m")
    
    # print(json.dumps(apple_candles, indent=2))
    # print(candles)
    print(f"--- Retrieved {len(candles)} Candles ---")
    