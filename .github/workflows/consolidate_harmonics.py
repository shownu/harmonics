import pandas as pd
import numpy as np
import time

min_fundamental = 5
time_period = 300
      
from_csv = pd.read_csv(r'XXXXXXXXXXXXXXXXXXX.csv')
orig = from_csv[from_csv.fundamental > min_fundamental]
orig = orig.sort_values(by=['time'])
max_sec = min(orig['time']) + time_period

while not orig.empty:
    group = orig[orig.time <= max_sec]
    sec_values = [max_sec-time_period, max_sec]
    final = len(sec_values) - 1
    start_time = time.strftime('%H:%M:%S', time.gmtime(sec_values[0]))
    end_time = time.strftime('%H:%M:%S', time.gmtime(sec_values[final]))
    elapsed = sec_values[final] - sec_values[0]
    elapsed = time.strftime('%M m %S s', time.gmtime(elapsed))
    print("-------------")
    print("from", start_time, "to", end_time, "-", elapsed)
    print("")
    if group.empty:
        print("***NO VESSELS DETECTED***")
    else:
        sec_values = group.time.tolist()
        df = orig[orig.time.isin(sec_values)]
        all_beam_values = df.beam.unique()
        all_beam_values = np.sort(all_beam_values)
        for i in range(len(all_beam_values)):
            beam_value = all_beam_values[i]
            beam_df = df[df['beam'] == beam_value]
            f = beam_df['fundamental'].unique().tolist()
            f = np.sort(f)
            f = f.tolist()
#        print("at beam", beam_value, "initially", f)
            j = 0
            while j < len(f):
                sig_freq = f[j]              
                sig_multiples = np.arange(sig_freq, max(f)+1, sig_freq).tolist()
                intersection = list(set(f).intersection(sig_multiples))
                intersection = np.sort(intersection).tolist()
                if len(intersection) > 1:
                    del intersection[0]
                    f = [x for x in f if x not in intersection]
                f = np.sort(f)
                f = f.tolist()
                j = j + 1
            print("at beam", beam_value, "detected", f)
    orig = pd.concat([orig, group]).drop_duplicates(keep=False)
    max_sec = max_sec + time_period
