import tkinter as tk
from threading import Thread
from tkinter import messagebox, filedialog
from tkinter.ttk import Notebook
import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.gui.widgets import common_input_form, TabNarma, TabPulse, TabSweep, Statusbar, Sidebar, HistoryWindow

from src.core.database import create_users_table, append_record_users, refer_users_table, create_materials_table, append_record_materials, refer_materials_table, create_samples_table, append_record_samples, refer_samples_table, create_pulse_templetes_table, create_sweep_templetes_table, create_measures_types_table, create_history_table, append_record_measure_types, fetch_measure_type_index

from src.core import narma_run, CommonParameters, PulseParameters, SweepParam, NarmaParam, timer, pulse_run, sweep_run


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Pulse ver2.1")
        self.pack(fill="both", expand=True)

        self.main_window = MainWindow(master=self)
        self.history_window = HistoryWindow(master=self)

        self.sidebar = Sidebar(master=self, contents=[self.main_window, self.history_window])

    #     self.__statusbar = Statusbar(master=self)
    
    # @property
    # def status_bar(self):
    #     return self.__statusbar


class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack(fill="both", expand=True, side="right")
        self.form_top = common_input_form(self)

        tab_classes = [TabNarma, TabPulse, TabSweep]
        tab_name = ["NARMA", "Pulse", "I-Vsweep"]

        self.notebook = Notebook(master=self)

        self.tab_instances = []
        for cls, name in zip(tab_classes, tab_name):
            instance = cls(master=self.notebook)
            self.tab_instances.append(instance)
            self.notebook.add(instance, text=name)

        self.notebook.pack(fill="both", expand=True)

        self.exe_button = tk.Button(master=self, text="実行", command=self.click_exe_button)
        self.exe_button.pack(side="top", pady=10)

    @property
    def pulse_blocks(self):
        return self.tab_instances[1].pulse_blocks

    def click_exe_button(self):
        """
        実行ボタン押下後の処理
        """
        file_path = ""
        is_output_excel_file = messagebox.askyesno("確認", "ファイル出力しますか？")
        if is_output_excel_file:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialdir=f'C:/Users/higuchi/Desktop/{self.form_top.input_measure_person}',
                initialfile=f'{self.form_top.input_material_name}_{self.form_top.input_sample_num}_{self.form_top.input_option}'
            )
        print(file_path)
        common_param: CommonParameters = {
            'user_name': self.form_top.input_measure_person,
            'material': self.form_top.input_material_name,
            'sample_num': self.form_top.input_sample_num,
            'file_path': file_path
        }

        if not common_param['user_name'] == "":
            append_record_users(common_param['user_name'])
            self.form_top.user_name_list = refer_users_table()

        if not common_param['material'] == "":
            append_record_materials(common_param['material'])
            self.form_top.materials = refer_materials_table()

        if not common_param['sample_num'] == "":
            append_record_samples(common_param['material'], common_param['sample_num'])
            self.form_top.samples = refer_samples_table(common_param['material'])

        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 0:
            parameters = NarmaParam(
                use_database=self.tab_instances[0].is_use_prepared_array,
                model=self.tab_instances[0].narma_model,
                pulse_width=self.tab_instances[0].pulse_width,
                off_width=self.tab_instances[0].off_width,
                tick=self.tab_instances[0].tick,
                nodes=self.tab_instances[0].nodes,
                discrete_time=self.tab_instances[0].discrete_time,
                bot_voltage=self.tab_instances[0].bot_voltage,
                top_voltage=self.tab_instances[0].top_voltage,
                base_voltage=self.tab_instances[0].base_voltage
            )

            measure_type_index = fetch_measure_type_index("NARMA")

            # self.exe_thread = Thread(target=narma_run, args=(parameters, common_param))
            # self.exe_thread.start()

        if selected_tab == 1:
            standarded_pulse_blocks = self.pulse_blocks.export_standarded_blocks()
            tot_time = 0
            for block in standarded_pulse_blocks:
                tot_time += (block.top_time + block.base_time + block.interval) * block.loop

            parameters: PulseParameters = {
                'measure_blocks': self.pulse_blocks
            }
            measure_type_index = fetch_measure_type_index("2-terminate Pulse")
            self.timer_thread = Thread(target=timer, args=(tot_time, self.status_bar))
            self.timer_thread.start()

            self.exe_pulse_thread = Thread(target=pulse_run, args=(parameters, common_param))
            self.exe_pulse_thread.start()

        if selected_tab == 2:
            parameters = SweepParam(
                mode=self.tab_instances[2].sweep_mode,
                top_voltage=self.tab_instances[2].top_voltage,
                bottom_voltage=self.tab_instances[2].bottom_voltage,
                voltage_step=self.tab_instances[2].voltage_step,
                loop=self.tab_instances[2].loop,
                tick_time=self.tab_instances[2].tick
            )
            measure_type_index = fetch_measure_type_index("2-terminate I-Vsweep")

            self.exe_sweep_thread = Thread(target=sweep_run, args=(parameters, common_param))
            self.exe_sweep_thread.start()


if __name__ == "__main__":
    create_users_table()
    create_materials_table()
    create_samples_table()
    create_pulse_templetes_table()
    create_sweep_templetes_table()
    create_measures_types_table()
    append_record_measure_types("NARMA")
    append_record_measure_types("2-terminate I-Vsweep")
    append_record_measure_types("2-terminate Pulse")
    create_history_table()
    root = tk.Tk()
    # root.geometry("530x300")
    # root.resizable(False, False)#ウィンドウサイズをフリーズ
    root.lift()#最前面に表示
    app = Application(master=root)
    app.mainloop()

