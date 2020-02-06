import pandas as pd
import numpy as np
      
from_csv = pd.read_csv(r'XXXXXXXXXXXXXXXXXXXX.csv')

df = from_csv[from_csv.fundamental > 5]

all_beam_values = df.beam.unique()
all_beam_values = np.sort(all_beam_values)

for i in range(len(all_beam_values)):
    beam_value = all_beam_values[i]
    beam_df = df[df['beam'] == beam_value]
    f = beam_df['fundamental'].unique().tolist()
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
    print("in beam", beam_value, "found", f)
