# パルス測定プログラム

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from src.gui import Application
from src.database import initialize_db, append_record_measure_types

def main():
    initialize_db()
    append_record_measure_types("NARMA")
    append_record_measure_types("2-terminal I-Vsweep")
    append_record_measure_types("2-terminal Pulse")
    root = tk.Tk()
    #root.geometry("530x300")
    #root.resizable(False, False)#ウィンドウサイズをフリーズ
    root.lift()#最前面に表示
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()