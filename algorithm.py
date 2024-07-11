import time
import tkinter as tk
from operator import attrgetter

class Measure_block():
  instances = []
  stop_flag = False

  def __init__(self, loop=5, V_top=1.0, V_base=0.0, top_time=10.0, base_time=10.0, interval=10.0, spinbox_instances=None):
    self.set(len(Measure_block.instances), loop, V_top, V_base, top_time, base_time, interval, spinbox_instances)
    # Block_label(self)
    Measure_block.instances.append(self)

  # def __del__(self):


  @classmethod
  def reset_index(cls):
    for index, instance in enumerate(cls.instances):
      instance.index = index

  @classmethod
  def reset_selected(cls):
    for instance in cls.instances:
      instance.selected = False

  def set(self, index, loop, V_top, V_base, top_time, base_time, interval, spinbox_instances):
    self.index = index
    self.params = {
      "V_top" : V_top,
      "top_time" : top_time,
      "V_bot" : V_base,
      "bot_time" : base_time,
      "loop" : loop,
      "interval" : interval
    }

    self.select(spinbox_instances)

  def estimate_time(self):
    # for key, var in self.params:
    #   print("{}, {}".format(var, type(var)))
    return (float(self.params["bot_time"]) + float(self.params["top_time"])) * int(float(self.params["loop"])) + float(self.params["interval"])
  
  # def estimate_point(self):
  #   return (self.params["bot_time"] + self.params["top_time"]) * self.params["loop"] + self.params["interval"]

  def measure(self, V_set, measure_times, dev, datas, start_time):
    interval = 0.041463354054055365
    measure_points = int(measure_times/interval)
    self.stop_flag = False
    print(measure_points)
    for _ in range(measure_points):
        if Measure_block.stop_flag == True:
            break
        
        dev.write(f"SOV{V_set}")
        dev.write("*TRG")
        datas.time_list.append(time.perf_counter()-start_time)
        
        A=dev.query("N?")
        A_=float(A[3:-2])
        datas.A_list.append(A_)
        
        V=dev.query("SOV?")
        V_=float(V[3:-2])
        datas.V_list.append(V_)

  def run(self, dev, datas, start_time):
    for _ in range(int(float(self.params["loop"]))):
      self.measure(float(self.params["V_bot"]), float(self.params["bot_time"]), dev, datas, start_time)
      self.measure(float(self.params["V_top"]), float(self.params["top_time"]), dev, datas, start_time)

    self.measure(float(self.params["V_bot"]), float(self.params["interval"]), dev, datas, start_time)

  def select(self, spinbox_instances):
    Measure_block.reset_selected()
    for instance, (key, value) in zip(spinbox_instances, self.params.items()):
      instance.delete(0, tk.END)
      instance.insert(0, value)
    self.selected = True

  def delete(self):
    del self
    Measure_block.reset_index()

class Cycle():
  instances = []

  def __init__(self, loop=2):
    self.index = len(Cycle.instances)
    self.cycle_contents = []
    self.expect_time = 0.0
    self.loop = loop
    Cycle.instances.append(self)

  @classmethod
  def sort(cls):
    Cycle.instances.sort(key=attrgetter('cycle_contents[0].index'))

  @classmethod
  def reset_selected(cls):
    for instance in cls.instances:
      instance.selected = False

  def read(self):
    return self.cycle_contents

  def set(self, content):
    self.cycle_contents.append(content)
    self.expect_time = self.expect_time + content.estimate_time()
    self.cycle_contents.sort(key=attrgetter('index'))

  def select(self, spinbox):
    Cycle.reset_selected()
    spinbox.delete(0, tk.END)
    spinbox.insert(0, self.loop)
    self.selected = True

  def remove(self, content):
    self.cycle_contents.remove(content)

  def run(self, dev, datas, start_time):
    for _ in range(int(self.loop)):
      for block in self.cycle_contents:
        block.run(dev, datas, start_time)

class Measure_list():
  def __init__(self):
    self.blocks = Measure_block.instances
    self.cycles = Cycle.instances

  # def num_point(self):
  #   self.expect_point = 0
  #   for instance in self.blocks:
  #     self.expect_point = self.expect_point + instance.estimate_point()

  #   for instance in self.cycles:
  #     self.expect_point = self.expect_point + instance.expect_point
  #   return self.expect_point

  def cluc_tot_time(self):
    self.expect_time = 0.0
    for block in self.blocks:
      self.expect_time = self.expect_time + block.estimate_time()

    for cycle in self.cycles:
      self.expect_time = self.expect_time + cycle.expect_time
    return self.expect_time

  def make_block(self, spinbox_instances):
    new_block = Measure_block(spinbox_instances=spinbox_instances)
    self.blocks = Measure_block.instances
    return new_block

  def make_cycle(self):
    new_cycle = Cycle()
    self.cycles = Cycle.instances
    return new_cycle

  def add_block_to_cycle(self, content):
    Cycle.set(content)
    self.blocks.pop(content)

  def remove_cycle_content(self, index):
    popped = Cycle.remove(index)
    self.blocks.append(popped)

  def run(self, dev, datas):
    self.measure_list = self.blocks
    count = 0
    for cycle in self.cycles:
      self.measure_list.insert(cycle.cycle_contents[0].index - count, cycle)
      count = count + len(cycle.cycle_contents) - 1

    start_time = time.perf_counter()
    for measure in self.measure_list:
      measure.run(dev, datas, start_time)
