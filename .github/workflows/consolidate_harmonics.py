import pandas as pd
import numpy as np
import time

min_fundamental = 5
group_size = 6
      
from_csv = pd.read_csv(r'XXXXXXXXXXXXXXX.csv')
orig = from_csv[from_csv.fundamental > min_fundamental]
orig = orig.sort_values(by=['time'])

while not orig.empty:
    group = orig.head(group_size)
    sec_values = group.time.tolist()
    final = len(sec_values) - 1
    start_time = time.strftime('%H:%M:%S', time.gmtime(sec_values[0]))
    end_time = time.strftime('%H:%M:%S', time.gmtime(sec_values[final]))
    elapsed = sec_values[final] - sec_values[0]
    elapsed = time.strftime('%H h %M min %S sec', time.gmtime(elapsed))
    print("-------------")
    print("from", start_time, "to", end_time, "-", elapsed)
    print("")
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
