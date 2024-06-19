import tkinter as tk
from tkinter import filedialog
import time
import threading
import os
import pyvisa as visa
# from algorithm import Measure_frame, Measure_block
from graph import graph, livegraph
from data import Datas

interval_time = 0.041463354054055365#[s] 実行環境によって異なるので適時調整

rm = visa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')
dev = rm.open_resource('GPIB1::1::INSTR')
dev.timeout = 5000

#送信コマンド
def write(command):
    dev.write(command)

def set_folder_func(textbox):
    dir = 'C:\\'
    folder_path = filedialog.askdirectory(initialdir = dir)
    textbox["folderpath"].delete(0, tk.END)
    textbox["folderpath"].insert(tk.END, folder_path)       

def stop_func(statusbar):
    global stop_flag
    stop_flag = True
    statusbar.swrite("測定中断")

def timer(measure_times, statusbar):
    global time_list, timer_flag
    start_time = time.perf_counter()
    while 1:
        if timer_flag == True:
            statusbar.swrite(f"合計時間: {time.perf_counter()-start_time:.1f} [s]")
            break
        statusbar.swrite(f"経過時間: {time.perf_counter()-start_time:.1f} [s]" + "," + f"{len(time_list)}/" + str(measure_times))
        time.sleep(0.1)

#実行
def run_func(read_widgets, blocks, datas, statusbar):
    global A_list, V_list, time_list, stop_flag, timer_flag, livegraph_flag
    global interval_list#debug用
    stop_flag = False
    V_list, A_list, time_list =[], [], []
    
    #値を取得
    paras = {}
    for widget in read_widgets:
      try:
        paras = dict(**paras, **widget.get())
      except TypeError as e:
        print("エラー内容:",e)
    
    # loop = float(paras["ループ回数"])
    # V_bot = float(paras["V_bot"])
    # V_top = float(paras["V_top"])
    # top_time = float(paras["top_time"])#[s]
    # bot_time = float(paras["bot_time"])#[s]
    # hip_time = float(paras["おしり"])
    
    chk0 = paras["ファイルに出力しない"].get()
    chk1 = paras["測定終了後、プロットを表示する"].get()
    chk2 = paras["測定終了後、散布図を表示する"].get()
    chk3 = paras["タイマーを無効にする"].get()
    chk4 = paras["ライブ描画を有効にする"].get()
    extension_box_index = paras["ext"].current()
    extension = paras["ext"].get()
    
    # bot_times = int(bot_time/2/interval_time)#切り捨て
    # top_times = int(top_time/interval_time)#切り捨て
    # hip_times = int(hip_time/interval_time) - bot_times#切り捨て
    # if hip_times > 0: 
    #     measuretimes = (bot_times*2+top_times)*int(loop) + hip_times
    # else:
    #     measuretimes = (bot_times*2+top_times)*int(loop)
    
    #エラーチェック
    if not chk0 == True:
        folderpath = paras["folderpath"].get()
        filename = paras["filename"].get()
        if not os.path.exists(folderpath):
            statusbar.swrite("無効なフォルダーパスです")
            return
        filepath = folderpath +'/' + filename + extension

    for instance in blocks.instances:
        if instance.params["bot_time"] < interval_time:
            statusbar.swrite("bot_timeが短すぎます")
            return

        if instance.params["top_time"] < interval_time:
            statusbar.swrite("top_timeが短すぎます")
            return
        
        if instance.params["loop"].is_integer() == False:
            statusbar.swrite("ループ回数は整数値を設定してください")
            return

    #測定装置の準備
    start_commands = [
        "*RST",#初期化
        "M1",#トリガーモード HOLD
        "OH1",#ヘッダON
        "VF",#電圧発生
        "F2",#電流測定
        "MD0",#DCモード
        "R0",#オートレンジ
        "OPR"#出力
        ]
    for command in start_commands:
        try:
          dev.write(command)
        except:
          print(command)

    # dev.write("*RST")#初期化
    # dev.write("M1")#トリガーモード HOLD
    # dev.write("OH1")#ヘッダON
    # dev.write("VF")#電圧発生
    # dev.write("F2")#電流測定
    # dev.write("MD0")#DCモード
    # dev.write("R0")#オートレンジ
    # dev.write("OPR")#出力


    
    #測定タイマー起動
    if chk3 == False:
        timer_flag = False
        t1 = threading.Thread(target = timer, args = (blocks.cluc_tot_time,))
        t1.start()
    else:
        statusbar.swrite("測定中")
    #ライブ描画起動
    if chk4 == True:
        livegraph_flag = False
        t2 = threading.Thread(target = livegraph, args = (chk1, chk2))
        t2.start()
    #測定実行

    blocks.run(dev, datas)

    # for _ in range(int(loop)):
    #     measure(V_bot, bot_times, interval_time)         
    #     measure(V_top, top_times, interval_time)
    #     measure(V_bot, bot_times, interval_time)
    # if hip_times > 0:
    #     measure(V_bot, hip_times, interval_time)
    
    #タイマー終了
    if chk3 == False:
        timer_flag = True  
    else:
        statusbar.swrite("測定終了")
    #ライブ描画終了
    if chk4 == True:
        livegraph_flag = True
    
    write("SBY")
    
    #時間軸の作成
    interval_list = [time_list[i+1]-time_list[i] for i in range(len(time_list)-1)]
    totaltime_list = [sum(interval_list[:i]) for i in range(len(interval_list)+1)]

    graph(totaltime_list, A_list, V_list, chk1, chk2)
    
    #ファイルに出力する場合
    if not chk0 == True:
        datas.output(filepath, extension_box_index)

def exc_run_func(read_widgets, blocks, datas, statusbar):
    try:      
        t = threading.Thread(target = run_func(read_widgets, blocks, datas, statusbar))
        t.start()

    except:
        statusbar.swrite("予期せぬエラーです")
