import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
from widgets import Measure_box_frame

def generate_square_wave(V_top, top_time, V_base, base_time, loop):
    t_top = np.full(top_time, V_top)  # top_timeはサンプル数
    t_base = np.full(base_time, V_base)  # base_timeはサンプル数
    single_wave = np.concatenate((t_top, t_base))
    waveform = np.tile(single_wave, loop)  # loop回数だけ繰り返し
    return waveform

def combine_waveforms_with_intervals(waveform_list, intervals):
    combined_waveform = []

    for i, wave in enumerate(waveform_list):
        combined_waveform.append(wave)
        if i < len(waveform_list) - 1:
            interval_wave = np.full(intervals[i], 0)  # 各波形間の間隔
            combined_waveform.append(interval_wave)

    return np.concatenate(combined_waveform)

def plot_waveform(t, wave, title="Combined Square Waves"):
    plt.figure(figsize=(10, 4))
    plt.plot(t, wave, label='Square Wave')
    plt.title(title)
    plt.xlabel('Sample Number')
    plt.ylabel('Voltage [V]')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Parameters for the square waves
    #params_list = [{"V_top": 5, "top_time": 100, "V_base": 0, "base_time": 100, "loop": 3, "interval": 1000},{"V_top": 3, "top_time": 150, "V_base": -1, "base_time": 50, "loop": 2, "interval": 75}, {"V_top": 4, "top_time": 200, "V_base": 1, "base_time": 100, "loop": 4, "interval": 100}]

    list_of_dics = [Measure_box_frame.Measure_list.blocks,Measure_box_frame.Measure_list.circle]

    #waveforms = [generate_square_wave(params["V_top"], params["top_time"], params["V_base"], params["base_time"], params["loop"]) for params in params_list]
    #intervals = [params["interval"] for params in params_list]

    waveforms = [generate_square_wave(list["V_top"], list["top_time"], list["V_base"], list["base_time"], list["loop"]) for list in list_of_dics]
    intervals = [list["interval"] for list in list_of_dics]


    combined_wave = combine_waveforms_with_intervals(waveforms, intervals)
    total_samples = len(combined_wave)
    t = np.arange(total_samples)

    # Plot the combined square wave
    plot_waveform(t, combined_wave, title="Combined Square Waves with Intervals")
