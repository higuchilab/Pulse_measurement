import tkinter as tk
from tkinter import filedialog

def set_folder_func(textboxes: Any) -> callable:
    """フォルダ選択ダイアログを表示し、選択されたパスをテキストボックスに設定する関数を返します。"""
    def inner():
        dir = 'C:\\'
        folder_path = filedialog.askdirectory(initialdir=dir)
        textboxes.textbox["folderpath"].delete(0, tk.END)
        textboxes.textbox["folderpath"].insert(tk.END, folder_path)       
    return inner

def plot_and_save_data(datas: Datas, paras: Dict[str, Any]) -> None:
    """データのプロットと保存を行います。"""
    totaltime_list = calculate_total_time(datas.time_list)
    graph(totaltime_list, datas.V_list, datas.A_list, paras["測定終了後、プロットを表示する"].get(), paras["測定終了後、散布図を表示する"].get())
    
    if not paras["ファイルに出力しない"].get():
        filepath = os.path.join(paras["folderpath"].get(), paras["filename"].get() + paras["ext"].get())
        datas.output(filepath, paras["ext"].current())

def calculate_total_time(time_list: List[float]) -> List[float]:
    """累積時間リストを計算します。"""
    interval_list = [time_list[i+1] - time_list[i] for i in range(len(time_list) - 1)]
    return [sum(interval_list[:i]) for i in range(len(interval_list) + 1)]