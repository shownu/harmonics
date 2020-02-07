import pandas as pd
import numpy as np
import time
      
from_csv = pd.read_csv(r'XXXXXXXXXXXXXXXXXXXXXX.csv')
orig = from_csv[from_csv.fundamental > 5]

all_sec_values = orig.time.unique()
all_sec_values = np.sort(all_sec_values)

while not orig.empty:
    group = orig.head(8)
    final = len(group) - 1
    sec_values = group.time.tolist()
    start_time = time.strftime('%H:%M:%S', time.gmtime(sec_values[0]))
    end_time = time.strftime('%H:%M:%S', time.gmtime(sec_values[final]))
    print("-------------")
    print("from", start_time, "to", end_time)
    df = orig[orig.time.isin(sec_values)]
    all_beam_values = df.beam.unique()
    all_beam_values = np.sort(all_beam_values)
    for i in range(len(all_beam_values)):
        beam_value = all_beam_values[i]
        beam_df = df[df['beam'] == beam_value]
        f = beam_df['fundamental'].unique().tolist()
        f = np.sort(f)
        f = f.tolist()
#        print("in beam", beam_value, "initially", f)
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
