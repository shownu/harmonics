from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.colors
import seaborn as sns
import pandas as pd
import math

def samples_at_distance(direct_path):
    speed_of_sound = 1500 # m/s
    rx_depth = 100 # m
    em_depth = 100 # m
    multi_rx = math.sqrt((0.5*direct_path)**2 + rx_depth**2)
    multi_em = math.sqrt((0.5*direct_path)**2 + em_depth**2)
    multi = multi_rx + multi_em

    path_length_diff = multi - direct_path
    time_delay = path_length_diff / speed_of_sound
    no_samples = sample_rate * time_delay
    no_samples = int(no_samples)
    return no_samples

def find_x(y):
    threshold = 4*np.std(y)
    peaks = find_peaks(y, height=threshold)
    peak_val = peaks[1]['peak_heights']
    if peak_val.size > 0:
        peak_val = peak_val[0]
#        print("peak at", peak_val)
        x = np.where(y == peak_val)
        x = int(x[0])
#        print("at sample", x)
        return x
    
def add_vessel(z, approaching = True, bottom_bounce = False):
    mean = 0
    variance = 0.0004
    cepstrum_output = np.random.normal(loc=mean, scale=math.sqrt(variance), size=no_frames)
    if approaching == True:
        start = min_samples + z
        end = min_samples + z + 9
    else:
        start = max_samples - z - 9
        end = max_samples - z
    if bottom_bounce == True:
        cepstrum_output[start:end] = [-0.07, -0.1, -0.1, -0.12, -0.15, -0.12, -0.1, -0.1, -0.07]
        y = cepstrum_output[min_samples:max_samples]*-1
    else:
        cepstrum_output[start:end] = [0.07, 0.1, 0.1, 0.12, 0.15, 0.12, 0.1, 0.1, 0.07]
        y = cepstrum_output[min_samples:max_samples]
    return cepstrum_output, y

no_averages = 8
bool_plot = True

no_frames = 614400
sample_rate = 6000
fftsize = sample_rate

max_samples = samples_at_distance(100)
min_samples = samples_at_distance(2000)

samples_with_peak = []
now_vs_next = []
first = no_averages
last = int(no_frames/fftsize)-no_averages

for z in range(first, last):
    cepstrum_output, y = add_vessel(z, approaching = False, bottom_bounce = False)
    cepstrum_output = savgol_filter(cepstrum_output, 11, 3)
    if bool_plot == True:
        print(z)
        plt.figure(figsize=(15,5))
        plt.plot(cepstrum_output[min_samples:max_samples])
        plt.ylabel('Real Cepstrum')
        plt.xlabel('Samples')
        plt.grid(color='tab:gray', which='both', linestyle='--', linewidth=1)
        plt.show()
    x = find_x(y)
    samples_with_peak.append(x)
    
clean = [x for x in samples_with_peak if x != None]

for i in range(len(clean) - 1):
    bool_CPA = False
    bool_opening = False
    bool_closing = False    
    if clean[i] > clean[i+1]:
        now_vs_next.append(-1)
        bool_opening = True
    elif clean[i] == clean[i+1]:        
        now_vs_next.append(0)
        bool_CPA = True
    elif clean[i] < clean[i+1]:
        now_vs_next.append(1)
        bool_closing = True
        
if now_vs_next == []:
    print("no peaks detected!")
else:
    print("boxes below track change - red means moving closer, green moving away, and grey stationary. no of peaks found varies with chunk")
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["limegreen", "gainsboro", "crimson"])
    sns.set(rc={'figure.figsize':(20, 0.2)})
    d = {'col1': now_vs_next}
    df = pd.DataFrame(data = d)
    df = df.T
    plot = sns.heatmap(df, cbar = False, cmap = cmap, vmin = -1, vmax = 1)
    plt.show()
    overall = sum(now_vs_next)
    if overall < 0: # negative average means moving left over samples ie away
        print("overall, emitter moved further away")
    elif overall == 0:        
        print("overall, emitter stationary")
    elif overall > 0:
        print("overall, emitter moved closer")
    
print("-----------")
