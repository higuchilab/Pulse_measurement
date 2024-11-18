import tkinter as tk
from tkinter import Misc

class Sidebar(tk.Frame):
    def __init__(self, master: Misc, contents: list[tk.Frame]):
        super().__init__(master=master, width=150, bg="lightgray")
        self.pack(fill="both", expand=True, side="left")
        self.__contents = contents
        # サイドバーにボタンやラベルを追加
        label = tk.Label(self, text="サイドメニュー", bg="lightgray", font=("Arial", 14))
        label.pack(pady=10, fill="x")

        button1 = tk.Button(self, text="測定", command=self.open_measure_window)
        button1.pack(pady=5, fill="x")

        button2 = tk.Button(self, text="履歴", command=self.open_history_window)
        button2.pack(pady=5, fill="x")

        button3 = tk.Button(self, text="ボタン3")
        button3.pack(pady=5, fill="x")

        self.open_measure_window()

    @property
    def contents(self) -> list[tk.Frame]:
        return self.__contents

    def open_measure_window(self):
        for content in self.contents:
            content.pack_forget()
        self.contents[0].pack(fill="both", expand=True, side="right")

    def open_history_window(self):
        for content in self.contents:
            content.pack_forget()
        self.contents[1].pack(fill="both", expand=True, side="right")
