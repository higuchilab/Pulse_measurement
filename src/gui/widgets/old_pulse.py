import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Dict, List, Tuple, Any
from abc import ABCMeta, abstractmethod

from src.core.measurement import exc_run_func, stop_func
from src.core.measurement_model import Measure_block, Measure_model, Cycle
from src.utils import set_folder_func


class Labels:
    def __init__(self, master: tk.Tk):
        """ラベルを初期化します。"""
        self.master = master
        self.label: Dict[str, tk.Label] = {}
        self.label_list = [
            ['保存先のフォルダ', 'ファイル名を入力'],
            ['V_top [V]', 'top_time [s]', 'V_bot [V]', 'bot_time [s]', 'ループ回数', 'おしり [s]'],
            ['※有効の場合、若干ばらつきが増加'],
            ['ファイル形式']
        ]
        self.label_params = [
            [25, 0, 10, 30, True],
            [40, 0, 75, 25, False],
            [230, 0, 172, 0, False],
            [290, 0, 40, 0, True]
        ]
        self.label_config = [
            [tag_] + con + [i] for tag, con in zip(self.label_list, self.label_params) for i, tag_ in enumerate(tag)
        ]
        self.create(self.label_config)

    def create(self, config: List[List[Any]]) -> None:
        """ラベルを作成します。"""
        for var in config:
            bg = '#B0E0E6' if var[5] else None
            self.label[var[0]] = tk.Label(master=self.master, text=var[0], background=bg)
            self.label[var[0]].place(x=var[1] + var[2]*var[6], y=var[3] + var[4]*var[6])


class TextBoxes:
    def __init__(self, master: tk.Tk):
        """テキストボックスを初期化します。"""
        self.master = master
        self.textbox: Dict[str, tk.Entry] = {}
        self.textbox_config = {
            "folderpath": [38, 120, 10, 'C:/Users/higuchi/Desktop/パルス測定'],
            "filename": [25, 120, 40, ""],
        }
        self.create()

    def create(self) -> None:
        """テキストボックスを作成します。"""
        for key, var in self.textbox_config.items():
            self.textbox[key] = tk.Entry(master=self.master, width=var[0])
            self.textbox[key].place(x=var[1], y=var[2])
            self.textbox[key].insert(0, var[3])

    def get(self) -> Dict[str, tk.Entry]:
        """テキストボックスの内容を取得します。"""
        return self.textbox


class CustomSpinbox(tk.Spinbox, metaclass=ABCMeta):
    def __init__(self, 
                 master: tk.Tk = None, 
                 label: str = "", 
                 place: Tuple[int, int] = (0, 0),
                 from_: float = -1.0, 
                 to: float = 1.0, 
                 interval: float = 0.1, 
                 init: float = 0.0):
        """カスタムスピンボックスを初期化します。"""
        super().__init__(master, width=7, format='%3.1f')
        self.master = master
        self.label = label
        self.value = tk.DoubleVar(master=self)
        self.value.trace_add("write", self.value_changed)
        self._block = Measure_block
        self.config(
            textvariable=self.value,
            from_=from_,
            to=to,
            increment=interval
        )
        self.place(x=place[0], y=place[1])
        self.delete(0, tk.END)
        self.insert(0, init)

    @property
    def block(self):
        return self._block
    
    @block.setter
    def block(self, value: Measure_block) -> Measure_block:
        self._block = value

    @abstractmethod
    def value_changed(self, *arg):
        pass


class TopVoltageSpinbox(CustomSpinbox):
    def value_changed(self, *arg):
        self.block.V_top(self.value)


class BaseVoltageSpinbox(CustomSpinbox):
    def value_changed(self, *arg):
        self.block.V_base(self.value)


class TopTimeSpinbox(CustomSpinbox):
    def value_changed(self, *arg):
        self.block.top_time(self.value)


class BaseTimeSpinbox(CustomSpinbox):
    def value_changed(self, *arg):
        self.block.base_time(self.value)


class IntervalSpinbox(CustomSpinbox):
    def value_changed(self, *arg):
        self.block.interval(self.value)


class LoopSpinbox(CustomSpinbox):
    def value_changed(self, *arg):
        self.block.loop(self.value)



# class SpinboxMain(CustomSpinbox):
#     instances: List['SpinboxMain'] = []

#     def __init__(self, *args, **kwargs):
#         """メインスピンボックスを初期化します。"""
#         super().__init__(*args, **kwargs)
#         SpinboxMain.instances.append(self)


class SpinboxSub(CustomSpinbox):
    instances: List['SpinboxSub'] = []

    def __init__(self, master: tk.Tk = None, label: str = "", place: Tuple[int, int] = (0, 0),
                 from_: float = -1.0, to: float = 1.0, interval: float = 0.1, init: float = 0.0):
        """サブスピンボックスを初期化します。"""
        super().__init__(master, label, place, from_, to, interval, init)
        SpinboxSub.instances.append(self)

    @classmethod
    def reset(cls) -> None:
        """全てのサブスピンボックスをリセットします。"""
        for instance in cls.instances:
            instance.delete(0, tk.END)
            instance.insert(0, instance.init)

    def get(self) -> Dict[str, float]:
        """スピンボックスの値を取得します。"""
        return {self.label: float(self.value.get())}


class Buttons:
    def __init__(self, master: tk.Tk, read_widgets: List[Any], blocks: Any, datas: Any, statusbar: Any):
        """ボタンを初期化します。"""
        self.master = master
        self.button: Dict[str, tk.Button] = {}
        self.button_list = ['フォルダ選択', '実行', '中断']
        self.button_func = [
            set_folder_func(read_widgets[0]),
            exc_run_func(read_widgets, blocks, datas, statusbar),
            lambda: stop_func(statusbar)
        ]
        self.button_params = [
            [10, 70],  # フォルダ選択
            [120, 70],  # 実行
            [230, 70]  # 中断
        ]
        self.button_config = [[tag] + con for tag, con in zip(self.button_list, self.button_params)]
        self.create(self.button_config)

    def create(self, config: List[List[Any]]) -> None:
        """ボタンを作成します。"""
        for var, func in zip(config, self.button_func):
            self.button[var[0]] = tk.Button(master=self.master, text=var[0], command=func)
            self.button[var[0]].place(x=var[1], y=var[2])


class CheckButtons:
    def __init__(self, master: tk.Tk):
        """チェックボタンを初期化します。"""
        self.master = master
        self.checkbutton: Dict[str, tk.BooleanVar] = {}
        self.checkbutton_config = {
            'ファイルに出力しない': False,
            '測定終了後、プロットを表示する': True,
            '測定終了後、散布図を表示する': False,
            'タイマーを無効にする': False,
            'ライブ描画を有効にする': False,
        }
        self.create(self.checkbutton_config)

    def create(self, config: Dict[str, bool]) -> None:
        """チェックボタンを作成します。"""
        for i, (key, var) in enumerate(config.items()):
            self.checkbutton[key] = tk.BooleanVar()
            self.checkbutton[key].set(var)
            chk = tk.Checkbutton(
                master=self.master,
                variable=self.checkbutton[key],
                text=key
            )
            chk.place(x=230, y=75 + 20*i)

    def get(self) -> Dict[str, tk.BooleanVar]:
        """チェックボタンの状態を取得します。"""
        return self.checkbutton


class ComboBoxes:
    def __init__(self, master: tk.Tk):
        """コンボボックスを初期化します。"""
        self.master = master
        self.combobox: Dict[str, ttk.Combobox] = {}
        self.combobox_config = {
            "ext": [4, [".txt", ".csv", ".xlsx"], 360, 40, 2],
        }
        self.create(self.combobox_config)

    def create(self, config: Dict[str, List[Any]]) -> None:
        """コンボボックスを作成します。"""
        for key, var in config.items():
            self.combobox[key] = ttk.Combobox(
                master=self.master,
                width=var[0],
                justify="left",
                state="readonly",
                values=var[1],
            )
            self.combobox[key].place(x=var[2], y=var[3])
            self.combobox[key].current(var[4])

    def get(self) -> Dict[str, ttk.Combobox]:
        """コンボボックスの選択値を取得します。"""
        return self.combobox


class MeasureBoxFrame(tk.Frame):
    def __init__(self, master: tk.Tk):
        """測定ボックスフレームを初期化します。"""
        super().__init__(master)
        self.master = master
        self.config(relief="groove", width=80, height=200, bd=2)
        self.measure_list = Measure_model()
        self.init_block = BlockLabelMain(master=self)
        self.init_block.open_setting()
        MeasureBoxCnfButtons(master=self.master, frame=self)
        self.place(x=430, y=0)


class MeasureFrameSub(tk.Frame):
    def __init__(self, master: tk.Tk, **kwargs):
        """測定フレームサブを初期化します。"""
        super().__init__(master, **kwargs)
        self.config(relief="groove", width=80, height=200, bd=2)
        for block_label in BlockLabelMain.instances:
            BlockLabelSub(self, block_label)
        self.place(x=10, y=10)

    def pos_label(self) -> None:
        """ラベルの位置を更新します。"""
        for i, ins in enumerate(BlockLabelMain.instances):
            new_label = BlockLabelSub(master=self, parent=ins)
            new_label.place(x=0, y=25*i)


class MeasureBoxCnfButtons:
    def __init__(self, master: tk.Tk, frame: MeasureBoxFrame):
        """測定ボックス設定ボタンを初期化します。"""
        self.master = master
        self.frame = frame
        self.add_button = tk.Button(master=self.master, text="Add", command=self.make_block)
        self.del_button = tk.Button(master=self.master, text="Del", command=self.del_block)
        self.del_button["state"] = tk.DISABLED
        self.cycle_button = tk.Button(master=self.master, text="Cycle set", command=self.open_cycle)
        self.add_button.place(x=440, y=250)
        self.del_button.place(x=480, y=250)
        self.cycle_button.place(x=380, y=250)

    def make_block(self) -> None:
        """ブロックを追加します。"""
        new_block = BlockLabelMain(master=self.frame)
        self.del_button["state"] = tk.NORMAL
        self.master.update_idletasks()

    def del_block(self) -> None:
        """ブロックを削除します。"""
        for instance in BlockLabelMain.instances:
            if instance.block.selected:
                Measure_block.instances.remove(instance.block)
                del instance.block
                BlockLabelMain.instances.remove(instance)
                instance.destroy()
        if len(Measure_block.instances) == 1:
            self.del_button["state"] = tk.DISABLED
        BlockLabelMain.reset_pos()

    def open_cycle(self) -> None:
        """サイクルウィンドウを開きます。"""
        WindowSub(self.frame.measure_list, self.master)


class WindowSub(tk.Toplevel):
    def __init__(self, measure_list: Measure_model, master: tk.Tk = None):
        """サイクルウィンドウを初期化します。"""
        super().__init__(master)
        self.grab_set()
        self.geometry("300x300")
        self.cycle = measure_list.cycles
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        # ウィジット配置
        MeasureFrameSub(master=self)
        self.num_lp = SpinboxSub(
            master=self,
            label="loop",
            place=(125, 75),
            from_=1,
            to=10000,
            interval=1,
            init=""
        )
        cyc_frame = CycleFrame(cycles=self.cycle, master=self, lp=self.num_lp)
        CycleCnfButtons(master=self, cycle_frame=cyc_frame, lp=self.num_lp)

    def on_close(self) -> None:
        """ウィンドウを閉じる際の処理を行います。"""
        error_list = []
        for ins in Cycle.instances:
            index_list = [Measure_block.instances.index(block) for block in ins.cycle_contents]
            if not sum(index_list) == (len(index_list)-1) * len(index_list) / 2 + index_list[0] * len(index_list):
                error_list.append(ins)
        if len(error_list) == 0:
            CycleLabel.instances = []
            CycleLabel.num = 0
            BlockLabelSub.instances = []
            SpinboxSub.instances = []
            super().destroy()
        else:
            error_txt = ""
            for cycle in error_list:
                pass


# class SpinboxMain(CustomSpinbox):
#     instances: List['SpinboxMain'] = []

#     def __init__(self, *args, **kwargs):
#         """メインスピンボックスを初期化します。"""
#         super().__init__(*args, **kwargs)
#         SpinboxMain.instances.append(self)

# class SpinboxSub(CustomSpinbox):
#     instances: List['SpinboxSub'] = []

#     def __init__(self, master: tk.Tk = None, label: str = "", place: Tuple[int, int] = (0, 0),
#                  from_: float = -1.0, to: float = 1.0, interval: float = 0.1, init: float = 0.0):
#         """サブスピンボックスを初期化します。"""
#         super().__init__(master, label, place, from_, to, interval, init)
#         SpinboxSub.instances.append(self)

#     @classmethod
#     def reset(cls) -> None:
#         """全てのサブスピンボックスをリセットします。"""
#         for instance in cls.instances:
#             instance.delete(0, tk.END)
#             instance.insert(0, instance.init)

#     def get(self) -> Dict[str, float]:
#         """スピンボックスの値を取得します。"""
#         return {self.label: float(self.value.get())}


# class Buttons:
#     def __init__(self, master: tk.Tk, read_widgets: List[Any], blocks: Any, datas: Any, statusbar: Any):
#         """ボタンを初期化します。"""
#         self.master = master
#         self.button: Dict[str, tk.Button] = {}
#         self.button_list = ['フォルダ選択', '実行', '中断']
#         self.button_func = [
#             set_folder_func(read_widgets[0]),
#             exc_run_func(read_widgets, blocks, datas, statusbar),
#             lambda: stop_func(statusbar)
#         ]
#         self.button_params = [
#             [360, 10],  # フォルダ選択
#             [120, 250],  # 実行
#             [230, 250]  # 中断
#         ]
#         self.button_config = [[tag] + con for tag, con in zip(self.button_list, self.button_params)]
#         self.create(self.button_config)

#     def create(self, config: List[List[Any]]) -> None:
#         """ボタンを作成します。"""
#         for var, func in zip(config, self.button_func):
#             self.button[var[0]] = tk.Button(master=self.master, text=var[0], command=func)
#             self.button[var[0]].place(x=var[1], y=var[2])


# class CheckButtons:
#     def __init__(self, master: tk.Tk):
#         """チェックボタンを初期化します。"""
#         self.master = master
#         self.checkbutton: Dict[str, tk.BooleanVar] = {}
#         self.checkbutton_config = {
#             'ファイルに出力しない': False,
#             '測定終了後、プロットを表示する': True,
#             '測定終了後、散布図を表示する': False,
#             'タイマーを無効にする': False,
#             'ライブ描画を有効にする': False,
#         }
#         self.create(self.checkbutton_config)

#     def create(self, config: Dict[str, bool]) -> None:
#         """チェックボタンを作成します。"""
#         for i, (key, var) in enumerate(config.items()):
#             self.checkbutton[key] = tk.BooleanVar()
#             self.checkbutton[key].set(var)
#             chk = tk.Checkbutton(
#                 master=self.master,
#                 variable=self.checkbutton[key],
#                 text=key
#             )
#             chk.place(x=230, y=75 + 20*i)

#     def get(self) -> Dict[str, tk.BooleanVar]:
#         """チェックボタンの状態を取得します。"""
#         return self.checkbutton


# class ComboBoxes:
#     def __init__(self, master: tk.Tk):
#         """コンボボックスを初期化します。"""
#         self.master = master
#         self.combobox: Dict[str, ttk.Combobox] = {}
#         self.combobox_config = {
#             "ext": [4, [".txt", ".csv", ".xlsx"], 360, 40, 2],
#         }
#         self.create(self.combobox_config)

#     def create(self, config: Dict[str, List[Any]]) -> None:
#         """コンボボックスを作成します。"""
#         for key, var in config.items():
#             self.combobox[key] = ttk.Combobox(
#                 master=self.master,
#                 width=var[0],
#                 justify="left",
#                 state="readonly",
#                 values=var[1],
#             )
#             self.combobox[key].place(x=var[2], y=var[3])
#             self.combobox[key].current(var[4])

#     def get(self) -> Dict[str, ttk.Combobox]:
#         """コンボボックスの選択値を取得します。"""
#         return self.combobox


# class MeasureBoxFrame(tk.Frame):
#     def __init__(self, master: tk.Tk):
#         """測定ボックスフレームを初期化します。"""
#         super().__init__(master)
#         self.master = master
#         self.config(relief="groove", width=80, height=200, bd=2)
#         self.measure_list = Measure_model()
#         self.init_block = BlockLabelMain(master=self)
#         self.init_block.open_setting()
#         MeasureBoxCnfButtons(master=self.master, frame=self)
#         self.place(x=430, y=0)


# class MeasureFrameSub(tk.Frame):
#     def __init__(self, master: tk.Tk, **kwargs):
#         """測定フレームサブを初期化します。"""
#         super().__init__(master, **kwargs)
#         self.config(relief="groove", width=80, height=200, bd=2)
#         for block_label in BlockLabelMain.instances:
#             BlockLabelSub(self, block_label)
#         self.place(x=10, y=10)

#     def pos_label(self) -> None:
#         """ラベルの位置を更新します。"""
#         for i, ins in enumerate(BlockLabelMain.instances):
#             new_label = BlockLabelSub(master=self, parent=ins)
#             new_label.place(x=0, y=25*i)


# class MeasureBoxCnfButtons:
#     def __init__(self, master: tk.Tk, frame: MeasureBoxFrame):
#         """測定ボックス設定ボタンを初期化します。"""
#         self.master = master
#         self.frame = frame
#         self.add_button = tk.Button(master=self.master, text="Add", command=self.make_block)
#         self.del_button = tk.Button(master=self.master, text="Del", command=self.del_block)
#         self.del_button["state"] = tk.DISABLED
#         self.cycle_button = tk.Button(master=self.master, text="Cycle set", command=self.open_cycle)
#         self.add_button.place(x=440, y=250)
#         self.del_button.place(x=480, y=250)
#         self.cycle_button.place(x=380, y=250)

#     def make_block(self) -> None:
#         """ブロックを追加します。"""
#         new_block = BlockLabelMain(master=self.frame)
#         self.del_button["state"] = tk.NORMAL
#         self.master.update_idletasks()

#     def del_block(self) -> None:
#         """ブロックを削除します。"""
#         for instance in BlockLabelMain.instances:
#             if instance.block.selected:
#                 Measure_block.instances.remove(instance.block)
#                 del instance.block
#                 BlockLabelMain.instances.remove(instance)
#                 instance.destroy()
#         if len(Measure_block.instances) == 1:
#             self.del_button["state"] = tk.DISABLED
#         BlockLabelMain.reset_pos()

#     def open_cycle(self) -> None:
#         """サイクルウィンドウを開きます。"""
#         WindowSub(self.frame.measure_list, self.master)


# class WindowSub(tk.Toplevel):
#     def __init__(self, measure_list: Measure_model, master: tk.Tk = None):
#         """サイクルウィンドウを初期化します。"""
#         super().__init__(master)
#         self.grab_set()
#         self.geometry("300x300")
#         self.cycle = measure_list.cycles
#         self.protocol("WM_DELETE_WINDOW", self.on_close)
#         # ウィジット配置
#         MeasureFrameSub(master=self)
#         self.num_lp = SpinboxSub(
#             master=self,
#             label="loop",
#             place=(125, 75),
#             from_=1,
#             to=10000,
#             interval=1,
#             init=""
#         )
#         cyc_frame = CycleFrame(cycles=self.cycle, master=self, lp=self.num_lp)
#         CycleCnfButtons(master=self, cycle_frame=cyc_frame, lp=self.num_lp)

#     def on_close(self) -> None:
#         """ウィンドウを閉じる際の処理を行います。"""
#         error_list = []
#         for ins in Cycle.instances:
#             index_list = [Measure_block.instances.index(block) for block in ins.cycle_contents]
#             if not sum(index_list) == (len(index_list)-1) * len(index_list) / 2 + index_list[0] * len(index_list):
#                 error_list.append(ins)
#         if len(error_list) == 0:
#             CycleLabel.instances = []
#             CycleLabel.num = 0
#             BlockLabelSub.instances = []
#             SpinboxSub.instances = []
#             super().destroy()
#         else:
#             error_txt = ""
#             for cycle in error_list:
#                 for label in CycleLabel.instances:
#                     if label.cycle == cycle:
#                         error_txt = error_txt + label.text.get() + " "
#             messagebox.showerror("エラー", f"{error_txt}の選択に飛びがあります")


class CycleFrame(tk.Frame):
    def __init__(self, cycles: List[Cycle], lp: SpinboxSub, **kwargs):
        """サイクルフレームを初期化します。"""
        super().__init__(**kwargs)
        self.lp = lp
        self.config(relief="groove", width=80, height=200, bd=2)
        self.place(x=200, y=10)
        for cycle in cycles:
            CycleLabel(cycle=cycle, lp=self.lp, master=self)

class CycleCnfButtons:
    def __init__(self, master: tk.Tk, cycle_frame: CycleFrame, lp: SpinboxSub):
        """サイクル設定ボタンを初期化します。"""
        self.master = master
        self.cycle_frame = cycle_frame
        self.lp = lp
        self.add_button = tk.Button(master=self.master, text="Add", command=self.make_cycle)
        self.del_button = tk.Button(master=self.master, text="Del", command=self.del_cycle)
        self.del_button["state"] = tk.DISABLED
        self.add_button.place(x=200, y=250)
        self.del_button.place(x=250, y=250)

    def make_cycle(self) -> None:
        """サイクルを追加します。"""
        new_cycle = CycleLabel(master=self.cycle_frame, cycle=None, lp=self.lp)
        self.del_button["state"] = tk.NORMAL
        self.master.update_idletasks()

    def del_cycle(self) -> None:
        """サイクルを削除します。"""
        for instance in CycleLabel.instances:
            if instance.selected:
                Cycle.instances.remove(instance.cycle)
                del instance.cycle
                CycleLabel.instances.remove(instance)
                instance.destroy()
        if len(Cycle.instances) == 1:
            self.del_button["state"] = tk.DISABLED
        CycleLabel.reset_pos()

class BlockLabelMain(tk.Label):
    instances: List['BlockLabelMain'] = []
    num = 0

    def __init__(self, master: tk.Tk, **kwargs):
        """ブロックラベルメインを初期化します。"""
        super().__init__(master, **kwargs)
        BlockLabelMain.instances.append(self)
        BlockLabelMain.num = BlockLabelMain.num + 1
        self.selected = False
        self.text = tk.StringVar(master=self, value=f"ブロック{BlockLabelMain.num}")
        self.config(
            textvariable=self.text,
            bg="white"
        )
        self.block = self.master.measure_list.make_block()
        self.bind("<ButtonPress-1>", self.open_setting)
        self.place(x=0, y=20*(len(BlockLabelMain.instances)))

    @classmethod
    def reset_bg(cls) -> None:
        """背景色をリセットします。"""
        for instance in cls.instances:
            instance.config(bg="white")

    @classmethod
    def reset_pos(cls) -> None:
        """位置をリセットします。"""
        for i, instance in enumerate(cls.instances):
            instance.place(x=0, y=20 * (i+1))

    def open_setting(self, event: tk.Event = None) -> None:
        """設定を開きます。"""
        # self.block.select()
        BlockLabelMain.reset_bg()
        self.config(bg="red")


class BlockLabelSub(tk.Label):
    instances: List['BlockLabelSub'] = []

    def __init__(self, master: tk.Tk, parent: BlockLabelMain, **kwargs):
        """ブロックラベルサブを初期化します。"""
        super().__init__(master, **kwargs)
        self.selected = False
        BlockLabelSub.instances.append(self)
        self.parent_label = parent
        self.config(
            textvariable=self.parent_label.text,
            bg="white"
        )
        self.block = self.parent_label.block
        self.bind("<ButtonPress-1>", self.select)
        self.place(x=0, y=20*(len(BlockLabelSub.instances)))

    @classmethod
    def reset_bg(cls) -> None:
        """背景色をリセットします。"""
        for instance in cls.instances:
            instance.config(bg="white")

    def select(self, event: tk.Event = None) -> None:
        """選択状態を切り替えます。"""
        self.selected = not self.selected
        cycle_list = [ins for ins in CycleLabel.instances if ins.selected]
        if self.selected:
            cycle_list[0].cycle.set(self.block)
            self.config(bg="red")
        else:
            cycle_list[0].cycle.remove(self.block)
            self.config(bg="white")


class CycleLabel(tk.Label):
    instances: List['CycleLabel'] = []
    num = 0

    def __init__(self, lp: SpinboxSub, cycle: Cycle = None, **kwargs):
        """サイクルラベルを初期化します。"""
        super().__init__(**kwargs)
        CycleLabel.instances.append(self)
        CycleLabel.num = CycleLabel.num + 1
        if cycle is None:
            self.cycle = Cycle()
        else:
            self.cycle = cycle
        self.selected = False
        self.text = tk.StringVar(master=self, value=f"サイクル{CycleLabel.num}")
        self.config(
            textvariable=self.text,
            bg="white"
        )
        self.place(x=0, y=20*(len(CycleLabel.instances)))

        self.bind("<ButtonPress-1>", self.open_setting)

    @classmethod
    def reset_bg(cls) -> None:
        """背景色をリセットします。"""
        for instance in cls.instances:
            instance.selected = False
            instance.config(bg="white")

    @classmethod
    def reset_pos(cls) -> None:
        """位置をリセットします。"""
        for i, instance in enumerate(cls.instances):
            instance.place(x=0, y=20 * (i+1))

    def open_setting(self, event: tk.Event = None) -> None:
        """設定を開きます。"""
        self.cycle.select(SpinboxSub.instances[0])
        CycleLabel.reset_bg()
        BlockLabelSub.reset_bg()
        contents = self.cycle.read()
        for block in BlockLabelSub.instances:
            for content in contents:
                if block.block == content:
                    block.selected = True
                    block.config(bg="red")
        self.selected = True
        self.config(bg="red")


