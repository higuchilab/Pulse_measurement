import tkinter as tk
from tkinter import ttk
from controller import set_folder_func, exc_run_func, stop_func
from algorithm import Measure_block, Measure_frame

class Labels():
  def __init__(self, master):
    self.master = master
    self.label = {}
    self.label_list = [['保存先のフォルダ', 'ファイル名を入力'],
                       ['V_top [V]', 'top_time [s]', 'V_bot [V]', 'bot_time [s]', 'ループ回数', 'おしり [s]'],
                       ['※有効の場合、若干ばらつきが増加'],
                       ['ファイル形式']]
    # x = a+bx, y=c+dxを満たす[a, b, c, d] + background
    self.label_params = [[25, 0, 10, 30, True],
                         [40, 0, 75, 25, False],
                         [230, 0, 172, 0, False],
                         [290, 0, 40, 0, True]]
    self.label_config = [[tag_] + con + [i] for tag, con in zip(self.label_list, self.label_params) for i, tag_ in enumerate(tag)]
    self.create(self.label_config)

  def create(self, config):
    for var in config:
      if var[5] == True:
        self.label[var[0]] = tk.Label(master=self.master, text= var[0], background= '#B0E0E6')
      else:
        self.label[var[0]] = tk.Label(master=self.master, text= var[0])
      self.label[var[0]].place(x=var[1] + var[2]*var[6], y= var[3] + var[4]*var[6])

class TextBoxes():
  def __init__(self, master):
    self.master = master
    self.textbox = {}
    self.textbox_config = {
      #{tag :[wid, x, y, init]}
      "folderpath" :[38, 120, 10, 'C:/Users/higuchi/Desktop/パルス測定'],
      "filename" :[25, 120, 40, ""],
      }
    self.create()

  def create(self):
    for key, var in self.textbox_config.items():
      self.textbox[key] = tk.Entry(master=self.master, width=var[0])
      self.textbox[key].place(x= var[1], y= var[2])
      self.textbox[key].insert(0, var[3])

  def get(self):
    return self.textbox #{"forderpath" : "", "filename" : ""}

class Spinbox(tk.Spinbox):
  instances = []
  
  def __init__(self, master=None, label="", place=(0,0), from_=-1.0, to=1.0, interval=0.1, init=0.0):
    super().__init__(master, width=7, format='%3.1f')
    self.master = master
    self.label = label
    Spinbox.instances.append(self)

    self.value = tk.DoubleVar(master=self)
    self.value.trace_add("write", self.callback)
    self.config(
      textvariable=self.value,
      from_=from_,
      to=to,
      increment=interval
    )
    self.place(x=place[0], y=place[1])
    self.insert(0, init)

  @classmethod
  def get_all(cls):
    return cls.instances
  
  def callback(self, arg1, arg2, arg3):
    for instance in Measure_block.instances:
      if instance.selected:
        instance[self.label] = arg1

  def ref_instances(self):
    return Spinbox.instances


# class SpinBoxes():
#   def __init__(self, master=None):
#     self.master = master
#     self.spinbox = {}
#     self.spinbox_config = {
#       #{tag :[min, max, step, init]}
#       "V_top" :[-30.0, 30.0, 0.1, 1.0],
#       "top_time" :[-30.0, 30.0, 0.1, 5.0],
#       "V_bot" :[-30.0, 30.0, 0.1, 0.0],
#       "bot_time" :[0.0, 10000.0, 0.1, 5.0],
#       "ループ回数":[1, 10000, 1, 5],
#       "インターバル(おしり)":[1, 10000, 0, 10],
#       }
#     self.create(self.spinbox_config)

#   def create(self, config):
#     for i, (key, var) in enumerate(config.items()):
#       value = tk.DoubleVar()
#       value.trace_add("write", self.callback)
#       self.spinbox[key] = tk.Spinbox(
#         master=self.master,
#         width = 7,
#         format = '%3.1f',
#         from_ = var[0],
#         to = var[1],
#         increment = var[2],
#         textvariable=value
#         )
#       self.spinbox[key].place(x= 125, y= 75 + 25*i)
#       self.spinbox[key].insert(0, var[3])

#   def get(self):
#     return self.spinbox # {"V_top", "top_time", "V_bot", "bot_time", "ループ回数", "インターバル(おしり)"}
  
#   def callback(self, arg1, arg2, arg3):
#     for instance in Measure_block.instances:
#       if instance.seledted:
#         instance.V_top = arg1


class Buttons():
  def __init__(self, master=None, read_widgets=None, measure_blocks=None, datas=None, statusbar=None):
    self.master = master
    self.read_widgets = read_widgets
    self.blocks = measure_blocks
    self.datas = datas
    self.button = {}
    self.button_config = {
      #{tag :[wid, pad_EW, pad_NS, x, y, command]}
      "参照": [8, 0, 0, 360, 9, set_folder_func],
      "実行": [12, 0, 10, 125, 225, exc_run_func(self.read_widgets, self.blocks, self.datas, statusbar)],
      "強制終了": [12, 0, 10, 225, 225, stop_func],
      }
    self.create(self.button_config)

  def create(self, config):
      for key, var in config.items():
          self.button[key] = ttk.Button(
              master=self.master,
              text = key,
              width = var[0],
              padding = [var[1], var[2]],
              command = var[5],
              )
          self.button[key].place(x= var[3], y= var[4])

class CheckButtons():
  def __init__(self, master=None):
    self.master = master
    self.checkbutton = {}
    self.checkbutton_config = {
      #[text :bln]
      'ファイルに出力しない' :False,
      '測定終了後、プロットを表示する' :True,
      '測定終了後、散布図を表示する' :False,
      'タイマーを無効にする' :False,
      'ライブ描画を有効にする' :False,
      }
    self.create(self.checkbutton_config)

  def create(self, config):
    for i, (key, var) in enumerate(config.items()):
      self.checkbutton[key] = tk.BooleanVar()
      self.checkbutton[key].set(var)
      chk = tk.Checkbutton(
        master=self.master,
        variable = self.checkbutton[key],
        text = key
        )
      chk.place(x= 230, y= 75 + 20*i)
  
  def get(self):
    return self.checkbutton

class ComboBoxes():
  def __init__(self, master):
    self.master = master
    self.combobox = {}
    self.combobox_config = {
      #tag :[wid, [values], x, y, init]
      "ext": [4, [".txt", ".csv", ".xlsx"], 360, 40, 2],       
      }
    self.create(self.combobox_config)

  def create(self, config):
    for key, var in config.items():
      self.combobox[key] = ttk.Combobox(
        master=self.master,
        width = var[0],
        justify = "left", 
        state = "readonly",
        values = var[1],
        )
      self.combobox[key].place(x= var[2], y= var[3])
      self.combobox[key].current(var[4])

  def get(self):
    return self.combobox

class Measure_box_frame(tk.Frame):
  def __init__(self, master):
    super().__init__(master)
    self.master = master
    self.config(relief="groove", width=80, height=200)
    self.measure_frame = Measure_frame()
    self.init_block = Block_label(master=self)
    self.add_button = tk.Button(master=self.master, text="Add", command=self.make_block)
    self.del_button = tk.Button(master=self.master, text="Del", command=self.del_block)
    self.del_button["state"] == "disable"
    self.cycle_button = tk.Button(master=self, text="Cycle set", command=self.open_cycle)
    self.add_button.place(x=440, y=250)
    self.del_button.place(x=480, y=250)
    self.place(x=430, y=0)

  def make_block(self):
    new_block = Block_label(master=self)
    # self.measure_frame.make_block()
    self.del_button["state"] == "able"
    self.master.update_idletasks()

  def del_block(self):
    #block_labelを消す処理を書く
    for instance in Block_label.instances:
      if instance.block.selected == True:
        del instance
        # self.measure_frame.del_block()
    if len(Measure_block.instances)==1:
      self.del_button["state"] == "disable"

  def open_cycle(self):
    self.window = tk.Toplevel(self.master)
    self.window.grab_set()

# class Measure_box_frame_option(tk.Frame):
#   def __init__(self, master):
#     super().__init__(master)
#     self.master=master

class Block_label(tk.Label):
  instances = []

  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    Block_label.instances.append(self)
    self.text=tk.StringVar(master=self, value="ブロック")
    self.config(
      textvariable=self.text,
      bg="white"
    )
    self.block = self.master.measure_frame.make_block()
    # self.block = Measure_block()
    # self.pack(side=tk.TOP)
    self.place(x=450, y=20*(len(Block_label.instances)))

    self.bind("<ButtonPress-1>", self.open_setting)

  def __del__(self):
    self.block.delete()
    Block_label.reset_pos()

  @classmethod
  def reset_bg(cls):
    cls.config(bg="white")

  @classmethod
  def reset_pos(cls):
    for i, instance in enumerate(cls.instances):
      instance.place(450, 20 * i)

  def open_setting(self):
    self.block.select(Spinbox.instances)
    self.config(bg="red")

class Statusbar(tk.Label):
  def __init__(self, master=None, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W):
    super().__init__(master, text=text, bd=bd, relief=relief, anchor=anchor)
    self.pack(side = tk.BOTTOM, fill = tk.X)

  def swrite(self, text):
    self["text"] = text
