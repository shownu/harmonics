from scipy.io import wavfile
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
#from tkinter import Tk, Label
from pydub import AudioSegment
from pydub.utils import make_chunks
import numpy as np
import matplotlib.colors
import seaborn as sns
import pandas as pd
import librosa
import math
import wave
#import time
 
#def popup():
#    dialog_box = Tk()
#    dialog_box.geometry('160x50+1000+600')
#    if bool_NA == True:
#        title = 'N/A'
#        Label(dialog_box, text = '-----', fg = 'gray', bg = 'gray').place(x = 10, y = 10)    
#    if bool_closing == True:
#        title = 'Closing'
#        Label(dialog_box, text = '-----', fg = 'red', bg = 'red').place(x = 10, y = 10)
#    if bool_CPA == True or bool_opening == True:
#        if bool_CPA == True: title = 'CPA'
#        if bool_opening == True: title = 'Opening'
#        Label(dialog_box, text = '-----', fg = 'limegreen', bg = 'limegreen').place(x = 10, y = 10)
#    Label(dialog_box, text = title).place(x = 50, y = 10)
#    return dialog_box.mainloop()

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
    
def real_cepstrum(x, n = None):
    w = np.ones(len(x))
    spectrum = np.fft.fft(x*w, n)
    ceps_real = np.fft.ifft(np.log(np.abs(spectrum))).real
    ceps_real[0] = 0.0
    return ceps_real

filename = 'XXXXXXXXXXXXXXXXXXXXXXXXX.wav'
split_into = 8

original_wav = AudioSegment.from_file(filename, "wav")
original_wav_length = librosa.get_duration(filename = filename) * 1000 # ms
chunk_length = original_wav_length / split_into
chunks = make_chunks(original_wav, chunk_length)
start_time = 0

for i, chunk in enumerate(chunks):
    chunk_name = "chunk_{0}.wav".format(i)
    chunk.export(chunk_name, format="wav")

    end_time = start_time + chunk_length/1000
    print("from", int(start_time), "sec to", int(end_time), "sec")

    obj = wave.open(chunk_name,'r')
    sample_rate = obj.getframerate()
    no_frames = obj.getnframes()
    obj.close() # what does this do?

    amplitudes = wavfile.read(chunk_name)[1]
    times = np.arange(len(amplitudes))/float(sample_rate)
    
    no_averages = 8
    fftsize = sample_rate
    max_samples = samples_at_distance(100)
    min_samples = samples_at_distance(2000)
    
    cepstrum_output = np.zeros(int(fftsize))
    samples_with_peak = []
    now_vs_next = []
    bool_plot = False
    
    for z in range(no_averages, int(no_frames/fftsize)-no_averages):
        for y in range (-no_averages, 0):
            timeseries = amplitudes[int((z-y)*fftsize):int((z-y+1)*fftsize)]
            cepstrum_output += real_cepstrum(timeseries)
        cepstrum_output = cepstrum_output/no_averages
        # Make a plot of averaged cepstrum
        if bool_plot == True:
            print(z)
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
    # clean.reverse() # for negative
    
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
    #    popup()
    #    time.sleep(0.5)
            
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
        
    start_time = end_time
    print("-----------")
