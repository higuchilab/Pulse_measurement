import tkinter as tk
from tkinter import filedialog
import time
import threading
import os
import pyvisa as visa
from graph import graph, livegraph
from data import Datas

interval_time = 0.041463354054055365#[s] 実行環境によって異なるので適時調整

rm = visa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')
dev = rm.open_resource('GPIB1::1::INSTR')
dev.timeout = 5000

#送信コマンド
def write(command):
    dev.write(command)

def set_folder_func(textboxes):
    def inner():
        dir = 'C:\\'
        folder_path = filedialog.askdirectory(initialdir = dir)
        textboxes.textbox["folderpath"].delete(0, tk.END)
        textboxes.textbox["folderpath"].insert(tk.END, folder_path)       
    return inner

def stop_func(statusbar):
    statusbar.swrite("測定中断")

def timer(measure_times, statusbar, timer_flag=False):
    start_time = time.perf_counter()
    while time.perf_counter()-start_time<measure_times:
        if timer_flag == True:
            statusbar.swrite(f"合計時間: {time.perf_counter()-start_time:.1f} [s]")
            break
        # statusbar.swrite(f"経過時間: {time.perf_counter()-start_time:.1f} [s]" + "/" + f"{len(datas.time_list)}/[s]")
        statusbar.swrite("{:.1f}/{:.1f}".format(time.perf_counter()-start_time, measure_times))
        time.sleep(0.1)

#実行
def run_func(read_widgets, blocks, datas, statusbar):
    # global A_list, V_list, time_list, stop_flag, timer_flag, livegraph_flag
    # global interval_list#debug用
    global timer_flag, livegraph_flag
    # stop_flag = False
    # V_list, A_list, time_list =[], [], []
    
    #値を取得
    paras = {}
    for widget in read_widgets:
      try:
        paras = dict(**paras, **widget.get())
      except TypeError as e:
        print("エラー内容:",e)
    
    chk0 = paras["ファイルに出力しない"].get()
    chk1 = paras["測定終了後、プロットを表示する"].get()
    chk2 = paras["測定終了後、散布図を表示する"].get()
    chk3 = paras["タイマーを無効にする"].get()
    chk4 = paras["ライブ描画を有効にする"].get()
    extension_box_index = paras["ext"].current()
    extension = paras["ext"].get()
    
    #エラーチェック
    if not chk0 == True:
        folderpath = paras["folderpath"].get()
        filename = paras["filename"].get()
        if not os.path.exists(folderpath):
            statusbar.swrite("無効なフォルダーパスです")
            return
        filepath = folderpath +'/' + filename + extension

    try:
        for block in blocks.blocks:
            if block.params["bot_time"] < interval_time:
                statusbar.swrite("bot_timeが短すぎます")
                return

            if block.params["top_time"] < interval_time:
                statusbar.swrite("top_timeが短すぎます")
                return
            
            if block.params["loop"].is_integer() == False:
                statusbar.swrite("ループ回数は整数値を設定してください")
                return
    except:
        pass


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

    #測定タイマー起動
    if chk3 == False:
        statusbar.swrite("timer start")
        timer_flag = False
        t1 = threading.Thread(target = timer, args = (blocks.cluc_tot_time(), statusbar, datas))
        t1.start()
    else:
        statusbar.swrite("測定中")
    #ライブ描画起動
    if chk4 == True:
        livegraph_flag = False
        t2 = threading.Thread(target = livegraph, args = (chk1, chk2))
        t2.start()
    #測定実行
    datas.reset()
    blocks.run(dev, datas)
    
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
    interval_list = [datas.time_list[i+1]-datas.time_list[i] for i in range(len(datas.time_list)-1)]
    totaltime_list = [sum(interval_list[:i]) for i in range(len(interval_list)+1)]

    graph(totaltime_list, datas.V_list, datas.A_list, chk1, chk2)
    
    #ファイルに出力する場合
    if not chk0 == True:
        datas.output(filepath, extension_box_index)

def exc_run_func(read_widgets, blocks, datas, statusbar):
    def inner():
        # try:      
        t = threading.Thread(target = run_func(read_widgets, blocks, datas, statusbar))
        t.start()

        # except:
        #     statusbar.swrite("予期せぬエラーです")
    return inner