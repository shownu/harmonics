import pandas as pd
import numpy as np
import random
import time

def compute_hcf(x, y):
   while(y):
       x, y = y, x % y
   return x
         
from_csv = pd.read_csv('XXXXXXXXXXXXXXX.csv')

no_of_trials = 1000
min_freq = 2
min_no_harmonics = 3
min_len = 3
len_f = 0
is_fundamental = False
ex = pd.DataFrame([])
print("working...")

all_sec_values = from_csv.time.unique()

for i in range(0, len(all_sec_values):
    sec_value = all_sec_values[i]
    sec_df = from_csv[from_csv['time'] == sec_value]    
    all_beam_values = sec_df.beam.unique()
    for j in range(0, len(all_beam_values)):
        beam_value = all_beam_values[j]
        df3 = sec_df[sec_df['beam'] == beam_value]
        
        freqs = df3['frequency']
        f = list(freqs)
        len_f = len(f)-1
        if len_f >= min_len:
#            print("found one longer than", min_len)

            df = pd.DataFrame([])
            
            count = 0
            while count < no_of_trials:
                x = random.randint(0, len(f)-1)    
                y = random.randint(0, len(f)-1)
                result = compute_hcf(f[x],f[y])
                if result > 1:
                    df = df.append(pd.DataFrame({"frequency":[result]}))
                    count = count + 1
        
            df2 = df['frequency'].value_counts()
            sig_val = len(df2.index)
            sig_val = 1/sig_val
            sig_val = sig_val*no_of_trials*2
#            print("checking for significant values...")
            
            df2_new = df2[df2 > sig_val]
    
            if df2_new.empty == False:
                index_len = len(df2_new.index)
                for k in range(0, index_len):
                    sig_freq = df2_new.index[k]                        
                    sig_multiples = np.arange(0, 200, sig_freq).tolist()
                    intersection = list(set(f).intersection(sig_multiples))
                    intersection = np.sort(intersection)
                    no_harmonics = len(intersection)
                    if sig_freq >= min_freq:
                        if no_harmonics >= min_no_harmonics:
                            hms = time.strftime('%H:%M:%S', time.gmtime(sec_value))
                            percentage = no_harmonics/len(f)
                            percentage = round(percentage, 2)
                            if intersection.size > 0:
                                first = intersection[0] % sig_freq
                                if first == 0:
                                    is_fundamental = True
                            ex = ex.append(pd.DataFrame({"time":[sec_value],
                                                         "hms": [hms],
                                                         "beam":[beam_value],
                                                         "fundamental":[sig_freq],
                                                         "pins to 0?":[is_fundamental],
                                                         "how many":[no_harmonics],
#                                                         "intersection":[intersection],
                                                         "as percentage":[percentage]}))
                            print("new entry added!")
                            is_fundamental = False
#                    else:
#                        print("significant value less than", min_frequency, "- trying new combination")
                        
            else:
#                print("not found, trying new combination")                       

                df2 = pd.DataFrame([])
                df2_new = pd.DataFrame([])
                len_f = 0
        
print(ex)
ex.to_csv(r'XXXXXXXXXXXXXX\output.csv', index=None, header=True)
