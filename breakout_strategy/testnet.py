import json
from breakout_strategy import emas, hma

def get_candles_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    

def get_ema(file_path, period):
    return emas.EMA.get_emas(candles)


def get_breakout_hma(indicator_candles):
    hmas = hma.BreakoutHMA(
        indicator_candles,
        55,
        5
    )

    return hmas.values()

    
    
if __name__ == '__main__':
    file_path = 'tests/test_data/candles.json'
    candles = get_candles_from_json(file_path)
    breakout_emas = get_breakout_hma(candles)

    print(json.dumps(breakout_emas, indent=4))
