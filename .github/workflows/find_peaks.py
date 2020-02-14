import math
import wave
import time
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from tkinter import Tk, Label

def popup():
    dialog_box = Tk()
    dialog_box.geometry('160x50+1000+600')
    if bool_closing == True:
        title = 'Closing'
        Label(dialog_box, text = '-----', fg = 'red', bg = 'red').place(x = 10, y = 10)
    if bool_CPA == True or bool_opening == True:
        if bool_CPA == True: title = 'CPA'
        if bool_opening == True: title = 'Opening'
        Label(dialog_box, text = '-----', fg = 'limegreen', bg = 'limegreen').place(x = 10, y = 10)
    Label(dialog_box, text = title).place(x = 50, y = 10)
    return dialog_box.mainloop()

def samples_at_distance(direct_path):
    speed_of_sound = 1500 # m/s
    rx_from_seabed = 100 # m
    em_from_seabed = 100 # m
    multi_rx = math.sqrt((0.5*direct_path)**2 + rx_from_seabed**2)
    multi_em = math.sqrt((0.5*direct_path)**2 + em_from_seabed**2)
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
    
def real_cepstrum(x, n=None):
    w = np.ones(len(x))
    spectrum = np.fft.fft(x*w, n)
    ceps_real = np.fft.ifft(np.log(np.abs(spectrum))).real
    ceps_real[0] = 0.0
    return ceps_real

filename = 'XXXXXXXXXXXXXXXXXXXXX.wav'
obj = wave.open(filename,'r')
sample_rate = obj.getframerate()
no_frames = obj.getnframes()
obj.close() # what does this do?

amplitudes = wavfile.read(filename)[1]
times = np.arange(len(amplitudes))/float(sample_rate)

no_averages = 8
fftsize = sample_rate
max_samples = samples_at_distance(100)
min_samples = samples_at_distance(2000)

cepstrum_output = np.zeros(int(fftsize))
samples_with_peak = []
now_vs_next = []
bool_plot = False

for z in range(no_averages,int(no_frames/fftsize)-no_averages):
    for y in range (-no_averages, 0):
        timeseries = amplitudes[int((z-y)*fftsize):int((z-y+1)*fftsize)]
        cepstrum_output += real_cepstrum(timeseries)
    cepstrum_output = cepstrum_output/no_averages
    # Make a plot of averaged cepstrum
    if bool_plot == True:
        print (z)
        plt.figure(figsize=(15,5))
        plt.plot(cepstrum_output[min_samples:max_samples])
        plt.ylabel('Real Cepstrum')
        plt.xlabel('Samples')
        plt.grid(color='tab:gray', which='both', linestyle='--', linewidth=1)
        plt.show()
    y = cepstrum_output[min_samples:max_samples]
    x = find_x(y)
    samples_with_peak.append(x)
    
clean = [x for x in samples_with_peak if x != None]
# clean.reverse()

for i in range(len(clean) - 1):
    bool_CPA = False
    bool_opening = False
    bool_closing = False    
    if clean[i] > clean[i+1]:
        now_vs_next.append(-1)
        bool_closing = True
    elif clean[i] == clean[i+1]:        
        now_vs_next.append(0)
        bool_CPA = True
    elif clean[i] < clean[i+1]:
        now_vs_next.append(1)
        bool_opening = True
#    popup()
#    time.sleep(0.5)
        
overall = sum(now_vs_next) 
if overall < 0: # negative sum means moving left over samples ie away
    print("overall, emitter moved further away")
elif overall == 0:        
    print("overall, emitter stationary")
elif overall > 0:
    print("overall, emitter moved closer")
