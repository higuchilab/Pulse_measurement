import tkinter as tk
from .widgets.old_pulse import Labels, TextBoxes, Buttons, CheckButtons, ComboBoxes, MeasureBoxFrame, Statusbar, CustomSpinbox, TopVoltageSpinbox, TopTimeSpinbox, BaseVoltageSpinbox, BaseTimeSpinbox, IntervalSpinbox, LoopSpinbox
from ..core.data_processing import Datas

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Pulse ver2.1")

        self.datas = Datas()

        self.setup_gui()

    def setup_gui(self):
        self.labels = Labels(master=self.master)
        self.text_boxes = TextBoxes(master=self.master)
        # self.setup_spinboxes()
        self.check_buttons = CheckButtons(master=self.master)
        self.combo_boxes = ComboBoxes(master=self.master)
        self.measure_box_frame = MeasureBoxFrame(master=self.master)
        self.statusbar = Statusbar(master=self.master)
        self.setup_buttons()

    def setup_spinboxes(self):
        self.spinbox_config = {
            "V_top": [-30.0, 30.0, 0.1, 1.0],
            "top_time": [-30.0, 30.0, 0.1, 5.0],
            "V_bot": [-30.0, 30.0, 0.1, 0.0],
            "bot_time": [0.0, 10000.0, 0.1, 5.0],
            "loop": [1, 10000, 1, 5],
            "interval": [1, 10000, 0, 10],
        }
        for i, (key, value) in enumerate(self.spinbox_config.items()):
            CustomSpinbox(
                master=self.master,
                label=key,
                place=(125, 75 + 25 * i),
                from_=value[0],
                to=value[1],
                interval=value[2],
                init=value[3]
            )

    def setup_buttons(self):
        self.buttons = Buttons(
            master=self.master,
            read_widgets=[
                self.text_boxes,
                self.check_buttons,
                self.combo_boxes
            ],
            blocks=self.measure_box_frame.measure_list,
            datas=self.datas,
            statusbar=self.statusbar
        )


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("530x300")
    root.resizable(False, False)#ウィンドウサイズをフリーズ
    root.lift()#最前面に表示
    app = Application(master=root)
    app.mainloop()

