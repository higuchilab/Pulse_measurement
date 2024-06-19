# -*- coding: utf-8 -*-
"""
2022/04/19
original
H. Uryu, 1521512@ed.tus.ac.jp(2023卒)

2022/4/28
Pulse化
R. Kaneko 1519032@ed.tus.ac.jp(2025卒)
K. Tomiyoshi 1522529@ed.tus.ac.jp(2024卒)

2022/5/1
GUI化、ファイル出力、強制終了ボタン、各種選択機能の追加
M. Taniguchi 1521536@ed.tus.ac.jp(2023卒)
"""
#default設定
# interval_time = 0.041463354054055365#[s] 実行環境によって異なるので適時調整
# d_V_bot = 0.1#[V]
# d_bot_time = 10#[s]
# d_V_top = 0.8#[V]
# d_top_time = 3.0#[s]
# d_loop = 2#回
# d_hip = 0#[s]
# d_folderpath = 'C:/Users/higuchi/Desktop/パルス測定'
# d_l_interval = 0.2#[s]ライブ描画の更新間隔
# d_x_label = "Time [s]"
# d_y1_label = "Voltage [V]"
# d_y2_label = "Current [A]"

import matplotlib.pyplot as plt
import tkinter as tk
from window import Application

class debug:
    def __init__(self, list1):
        self._x = list1
        
    #縦軸のみのグラフで表示、バラつき見る用 
    def dispersion(self):
        x = [1 for _ in range(len(self._x))]  
        fig = plt.figure()
        ax1 = fig.add_subplot()
        ax1.scatter(x, self._x)
        ax1.set_ylabel("Time [s]")
        plt.show()
        
    #平均値を取得
    def mean(self):
        print(sum(self._x)/len(self._x))
    
#     #時間軸の作成
#     interval_list = [time_list[i+1]-time_list[i] for i in range(len(time_list)-1)]
#     totaltime_list = [sum(interval_list[:i]) for i in range(len(interval_list)+1)]

if __name__ == "__main__":

    # rm = visa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')
    # dev = rm.open_resource('GPIB1::1::INSTR')
    # dev.timeout = 5000

    root = tk.Tk()
    root.title("Pulse ver1.1")
    root.geometry("530x300")#横×縦
    root.resizable(False, False)#ウィンドウサイズをフリーズ
    root.lift()#最前面に表示
    app = Application(root)
    app.mainloop()
