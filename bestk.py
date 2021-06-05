import pyupbit
import numpy as np
import time
import sys

def get_ror(symb, k=0.5):
    df = pyupbit.get_ohlcv(symb, count=30)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    #fee = 0.0032
    df['ror'] = np.where(df['high'] > df['target'],
                         #df['close'] / df['target'] - fee,
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("%s symb" % sys.argv[0])
        sys.exit(-1)
    symb = sys.argv[1]

    max_ror = -1
    max_k = 0.01
    for k in np.arange(0.01, 1.0, 0.01):
        ror = get_ror(symb, k)
        #print("%.2f %f" % (k, ror))
        if ror > max_ror:
            max_ror = ror
            max_k = k
        time.sleep(0.1)
    print("%.2f %f" % (max_k, max_ror))
