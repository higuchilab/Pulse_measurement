import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from src.gui.window_narma import Application

def main():
    root = tk.Tk()
    root.geometry("530x300")
    root.resizable(False, False)#ウィンドウサイズをフリーズ
    root.lift()#最前面に表示
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()