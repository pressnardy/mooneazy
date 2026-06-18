import requests


def get_candles(timeframe, quantity, symbol):
	"""
	excludes the last candle which is always an open candle
	"""
	url = 'https://api.binance.com/api/v3/klines'
	params = {
		'symbol': symbol,
		'interval': timeframe
	}
	response = requests.get(url, params=params).json()
	# print(response)
	candles = []
	for data in response:

		try:
			candle = {}
			open_time, open_price, high, low, close, volume, end_time = data[:7]
			candle['time'] = open_time
			candle['open'] = float(open_price)
			candle['high'] = float(high)
			candle['low'] = float(low)
			candle['close'] = float(close)
			candle['volume'] = float(volume)
			candle["end_time"] = end_time
			candles.append(candle)
		except Exception:
			raise ValueError("Big error")

	try:
		return candles[- quantity:-1]
	except ValueError:
		raise ValueError(f"maximum number of candles is 500")


def get_candles_from_time(symbol, interval, start_time, end_time):
	"""
	Fetch candlestick data from Binance API with a specified start time and end time.
	for calculating cvd
	"""
	base_url = "https://api.binance.com"
	endpoint = "/api/v3/klines"
	params = {
		"symbol": symbol,
		"interval": interval,
		"startTime": start_time,
		"endTime": end_time
	}
	url = f"{base_url}{endpoint}"
	response = requests.get(url, params=params).json()
	candles = []

	for data in response:
		try:
			candle = {}
			open_time, open_price, high, low, close, volume, end_time = data[:7]

			candle['open'] = float(open_price)
			candle['close'] = float(close)
			candle['volume'] = float(volume)
			candles.append(candle)
		except ValueError:
			raise ValueError

	return candles


def get_candles_from_params(**params):
	"""
	Fetch candlestick data from Binance API with a specified start time and end time.
	for calculating cvd
	"""
	base_url = "https://api.binance.com"
	endpoint = "/api/v3/klines"
	url = f"{base_url}{endpoint}"
	response = requests.get(url, params=params).json()
	candles = []

	for data in response:
		try:
			keys = ['time', 'open', 'high', 'low', 'close', 'volume', 'end_time']
			values = data[:7]
			candle = dict(zip(keys, values))
			candles.append(candle)
		except ValueError:
			raise ValueError('API Request Error')
	return candles


class Candles:
	def __init__(self, symbol, interval, start_time=None, end_time=None, quantity=None):
		self.params = {
			'symbol': symbol, 'interval': interval, 'startTime':start_time, 
			'endTime': end_time, 'limit': quantity
			}
		self._data = []

	@property
	def data(self):
		params = {k: v for k, v in self.params.items() if v}
		if not self._data:
			self._data = get_candles_from_params(params)
		return self._data
					
	

if __name__ == "__main__":
	timeframe = "4h"
	symbol = "BTCUSDT"
	quantity = 200
	print(get_candles(timeframe, quantity, symbol))
