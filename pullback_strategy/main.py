import json
from pullback_strategy.setups import get_setup_signal

def main():
    signals = get_setup_signal()
    print(json.dump(signals))

if __name__ == '__main__':
    main()
    


