from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
import tkinter as tk
from tkinter import Label, Entry, Frame, Variable, Misc, Toplevel, Button, StringVar, Radiobutton
from tkinter.ttk import Combobox, Treeview
from typing import Dict

from ....database import refer_users_table, refer_materials_table, refer_samples_table

class ComboboxForm(Frame):
    def __init__(
            self,
            label_name: str,
            input_width: int,
            values: list[str],
            master: Misc,
            textvariable: Variable,
            *arg
        ):
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


class RadioButtonForm(Frame):
    """
    ラジオボタンフォームのテンプレート
    """
    def __init__(self, master: Misc, form_name: str, values: list[tuple[str, str]], init: str):
        super().__init__(master=master)
        self.__select_item = StringVar(value=init)
        self.__label = Label(master=self, text=form_name)
        self.__label.pack(anchor=tk.W, side="top")
        for text, value in values:
            radio_button = Radiobutton(master=self, text=text, variable=self.__select_item, value=value)
            radio_button.pack(anchor=tk.W, side="top", padx=10)

    @property
    def select_item(self) -> str:
        return self.__select_item.get()


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
        self._input_material_name.trace_add("write", self.update_sample_list)
        self._material_name = ComboboxForm(label_name='物質名', input_width=5, values=refer_materials_table(), master=self.form_top, textvariable=self._input_material_name)
        self._material_name.pack(side="left", fill="y")

        self._input_sample_num = tk.StringVar()
        self._sample_num = ComboboxForm(label_name='試料No', input_width=5, values=refer_samples_table(self.input_material_name), master=self.form_top, textvariable=self._input_sample_num)
        self._sample_num.pack(side="left", fill="y")
        

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
    def materials(self, value: list[str]):
        self._material_name.combobox_values = value

    @property
    def samples(self) -> list[str]:
        return self._sample_num.combobox_values
    
    @samples.setter
    def samples(self, value: list[str]):
        self._sample_num.combobox_values = value

    def update_sample_list(self, *args):
        self.samples = refer_samples_table(self.input_material_name)


class Statusbar(Label):
    def __init__(self, master: tk.Tk = None, text: str = "", bd: int = 1, relief: str = tk.SUNKEN, anchor: str = tk.W):
        """ステータスバーを初期化します。"""
        super().__init__(master, text=text, bd=bd, relief=relief, anchor=anchor)
        self.pack(side=tk.BOTTOM, fill=tk.X)

    def swrite(self, text: str) -> None:
        """テキストを表示します。"""
        self["text"] = text


@dataclass
class TextVariables:
    param_names: list[str]
    variables: list[Variable]


class ParameterInputsForm(Frame, metaclass = ABCMeta):
    def __init__(
            self,
            master,
            text_variables: TextVariables
        ):
        super().__init__(master=master)
        self.__param_names = text_variables.param_names
        self.__top_label = Label(master=self, text="パラメーター")
        self.__top_label.pack(anchor=tk.W, side="top")
        self.__select_from_template_button = Button(master=self, text="テンプレートから選択", cursor='hand1', command=self.open_select_templete_window)
        self.__select_from_template_button.pack(anchor=tk.W, side="top", padx=10)

        for param_name, variable in zip(text_variables.param_names, text_variables.variables):
            entry_form = EntryForm(label_name=param_name, input_width=5, master=self, value=variable)
            entry_form.pack(anchor=tk.W, side="top", padx=10)

        self.__register_templete_button = Button(master=self, text="テンプレートに登録", cursor='hand1', command=self.register_templete)
        self.__register_templete_button.pack(anchor=tk.W, side="top", padx=10)

    @property
    def param_names(self) -> list[str]:
        return self.__param_names

    @abstractmethod
    def open_select_templete_window(self):
        pass

    @abstractmethod
    def recall_templete(self, values):
        pass

    @abstractmethod
    def register_templete(self):
        pass


class TempletesWindow(Toplevel, metaclass = ABCMeta):
    def __init__(self, master: Misc, main_window: ParameterInputsForm, columns: list[str]):
        super().__init__(master)
        self.title("Select Templete")
        self.main_window = main_window

        self.tree = Treeview(self, columns=columns, show="headings")
        for item in columns:
            self.tree.column(item, width=60, minwidth=60)
            self.tree.heading(item, text=item)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.select_button = Button(self, text="テンプレートを反映", command=self.set_values)
        self.select_button.pack(pady=10)

    def set_values(self):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            self.main_window.recall_templete(values)  # メインウィンドウのメソッドを呼び出して値を更新
        self.destroy()