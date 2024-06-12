import tkinter as tk
from tkinter import ttk
from widgets import Labels, TextBoxes, Spinbox, Buttons, CheckButtons, ComboBoxes, Measure_box_frame, Statusbar
from data import Datas

class Application(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    self.master.title("Pulse ver2.1")

    self.datas = Datas()

    self.labels = Labels(master=self.master)
    self.text_boxes = TextBoxes(master=self.master)
    # self.spin_boxes = SpinBoxes(master=self.master)

    self.spinbox_config = {
      #{tag :[min, max, step, init]}
      "V_top" :[-30.0, 30.0, 0.1, 1.0],
      "top_time" :[-30.0, 30.0, 0.1, 5.0],
      "V_bot" :[-30.0, 30.0, 0.1, 0.0],
      "bot_time" :[0.0, 10000.0, 0.1, 5.0],
      "loop":[1, 10000, 1, 5],
      "interval":[1, 10000, 0, 10],
      }
    for i, (key, value) in enumerate(self.spinbox_config.items()):
      Spinbox(
        master=self.master,
        label=key,
        place=(125, 75 + 25 * i),
        from_=value[0],
        to=value[1],
        interval=value[2],
        init=value[3]
      )

    self.check_buttons = CheckButtons(master=self.master)
    self.combo_boxes = ComboBoxes(master=self.master)

    self.measure_box_frame = Measure_box_frame(master=master)

    self.statusbar = Statusbar(master=self)

    self.buttons = Buttons(
      master=self.master,
      read_widgets=[
        self.text_boxes,
        self.check_buttons,
        self.combo_boxes],
      measure_blocks=self.measure_box_frame.measure_frame,
      datas=self.datas,
      statusbar=self.statusbar
      )

if __name__ == "__main__":
  root = tk.Tk()
  root.geometry("430x300")
  root.resizable(False, False)#ウィンドウサイズをフリーズ
  root.lift()#最前面に表示
  app = Application(master=root)
  app.mainloop()
