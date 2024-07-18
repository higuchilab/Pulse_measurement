import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd


# サンプルデータの作成
x = np.linspace(1, 1000, 1000)
A_list = np.log10(x)
V_list = np.log10(x / 2)
livegraph_flag = False

def graph(x_list, y1_list, y2_list):
    fig, (ax1, ax2) = plt.subplots(2, 1)

    ax1.tick_params(direction='in')
    ax2.tick_params(direction='in')

    ax1.set_xlabel("Time [s]", labelpad=1, font="Times New Roman", size=14)
    ax1.set_ylabel("Input Voltage [V]", labelpad=1, font="Times New Roman", size=14)
    ax2.set_xlabel("Time [s]", labelpad=1, font="Times New Roman", size=14)
    ax2.set_ylabel("Output Current [A]", labelpad=1, font="Times New Roman", size=14)

    ax1.plot(x_list, y1_list)
    ax2.plot(x_list, y2_list)
    plt.show()

def livegraph():
    global livegraph_flag, x, A_list, V_list

    time.sleep(1.0)
    while True:
        if livegraph_flag:
            break

        time_list_ = x
        V_list_ = V_list[:-1]  # インデックス範囲外エラーを避けるためにスライス
        A_list_ = A_list[:-1]  # インデックス範囲外エラーを避けるためにスライス
        interval_list = np.diff(x)  # 間隔を計算
        totaltime_list = np.cumsum(interval_list)  # 累積和で総時間を計算
        
        time.sleep(0.2)    
        
        graph(totaltime_list, V_list_, A_list_)

class GraphInput():
    def __init__(self, V_list, time_list):
        self.V_list = V_list
        self.time_list = time_list

V_top = 3
top_time = 10
V_base = 2
base_time = 15
loop = 3
interval = 20


# 初期グラフの表示
graph(x, A_list, V_list)

# ライブグラフ機能を実行するには、以下の行のコメントを解除してください
#livegraph_flag = True
#livegraph()
