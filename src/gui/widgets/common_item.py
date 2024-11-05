import tkinter as tk
from tkinter import Label, Entry, Frame, Variable, Misc
from tkinter.ttk import Combobox
from typing import List, Dict

from ...core.database import refer_users_table, refer_materials_table

class ComboboxForm(Frame):
    def __init__(self,
                 label_name: str,
                 input_width: int,
                 values: list[str],
                 master: Misc,
                 textvariable: Variable,
                 *arg):
        super().__init__(master, *arg)
        self.label = Label(master=self, text=label_name)
        self.label.pack(side="left", fill="y")
        self._combobox = Combobox(master=self, width=input_width, values=values, textvariable=textvariable)
        self._combobox.pack(side="left", fill="y")

    @property
    def combobox_values(self) -> list[str]:
        return self._combobox
    
    @combobox_values.setter
    def combobox_values(self, values):
        self._combobox['values'] = values


class EntryForm(Frame):
    """
    入力フォームとラベルのセット
    """
    def __init__(self, label_name: str, input_width: int, master: Misc, value: Variable, *arg):
        super().__init__(master, *arg)
        self.label = Label(master=self, text=label_name, width=10)
        self.label.pack(side="left", fill="y")
        self.combobox = Entry(master=self, width=input_width, textvariable=value)
        self.combobox.pack(side="left", fill="y")


def make_check_buttons(master: Misc):
    """チェックボタンを初期化します。"""
    checkbutton: Dict[str, tk.BooleanVar] = {}
    checkbutton_config = {
        'ファイルに出力しない': False,
        '測定終了後、プロットを表示する': True,
        '測定終了後、散布図を表示する': False,
        'タイマーを無効にする': False,
        'ライブ描画を有効にする': False,
    }

    for key, var in checkbutton_config.items():
        checkbutton[key] = tk.BooleanVar()
        checkbutton[key].set(var)
        chk = tk.Checkbutton(
            master=master,
            variable=checkbutton[key],
            text=key
        )
        chk.pack(anchor=tk.W, side="top", fill="x")


class common_input_form(Frame):
    """
    共通入力項目
    """
    def __init__(self, master: Misc):
        super().__init__(master=master)
        self.form_top = Frame(master=master, padx=5, pady=5)
        self.form_top.pack(side="top", fill="x", expand=True)

        self._input_measure_person = tk.StringVar()
        self._measure_person = ComboboxForm(label_name='測定者', input_width=10, values=refer_users_table(), master=self.form_top, textvariable=self._input_measure_person)
        self._measure_person.pack(side="left", fill="y")

        self._input_material_name = tk.StringVar()
        self._material_name = ComboboxForm(label_name='物質名', input_width=5, values=refer_materials_table(), master=self.form_top, textvariable=self._input_material_name)
        self._material_name.pack(side="left", fill="y")

        self._input_sample_num = tk.StringVar()
        self.sample_num = ComboboxForm(label_name='試料No', input_width=5, values=['1'], master=self.form_top, textvariable=self._input_sample_num)
        self.sample_num.pack(side="left", fill="y")
        

        self.form_bot = Frame(master=master, padx=5, pady=5)
        self.form_bot.pack(side="top", fill="x", expand=True)

        self._input_option = tk.StringVar()
        self.option_label = Label(master=self.form_bot, text='備考')
        self.option_label.pack(side="left", fill="y")
        self.option = Entry(master=self.form_bot, textvariable=self._input_option)
        self.option.pack(side="left", fill="y")

    @property
    def input_measure_person(self) -> str:
        return self._input_measure_person.get()
    
    @property
    def input_material_name(self) -> str:
        return self._input_material_name.get()
    
    @property
    def input_sample_num(self) -> str:
        return self._input_sample_num.get()
    
    @property
    def input_option(self) -> str:
        return self._input_option.get()
    
    @property
    def user_name_list(self) -> list[str]:
        return self._measure_person.combobox_values
    
    @user_name_list.setter
    def user_name_list(self, value):
        self._measure_person.combobox_values = value

    @property
    def materials(self) -> list[str]:
        return self._material_name.combobox_values
    
    @materials.setter
    def materials(self, value):
        self._material_name.combobox_values = value


class Statusbar(Label):
    def __init__(self, master: tk.Tk = None, text: str = "", bd: int = 1, relief: str = tk.SUNKEN, anchor: str = tk.W):
        """ステータスバーを初期化します。"""
        super().__init__(master, text=text, bd=bd, relief=relief, anchor=anchor)
        self.pack(side=tk.BOTTOM, fill=tk.X)

    def swrite(self, text: str) -> None:
        """テキストを表示します。"""
        self["text"] = text
