import pandas as pd
import numpy as np

df = pd.read_csv('dataset nov 1.csv')
ex = pd.DataFrame([])
tot_time = len(df.time.unique())

for i in range(0,tot_time):
    percentage = (i/tot_time)*100
    pval = round(percentage,2)
    print(pval, "% complete...") 
    sec_value = df.time.unique()[i]
    df2 = df[df['time'] == sec_value]
    unique_freq = np.sort(df2.frequency.unique())
    tot_freq = len(df2.frequency.unique())
    for j in range(0, tot_freq):
        freq_value = unique_freq[j]
        df3 = df2[df2['frequency'] == freq_value]
        largest_level = max(df3['level'])
        beam_max_level = df3.loc[df.level == largest_level, 'beam'].values[0]
        ex = ex.append(pd.DataFrame({"time":[sec_value],
                                     "frequency":[freq_value],
                                     "beam":[beam_max_level],
                                     "level":[largest_level]}))

ex = ex.sort_values(by=['time', 'beam', 'frequency'])
ex.to_csv(r'P:\Projects\2019\PT13_MEDUSA\05_Model\Laura Test Area\get max\output.csv', index=None, header=True)
print("100 % complete!")
