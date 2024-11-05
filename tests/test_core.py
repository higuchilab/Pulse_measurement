# テストコード
from src.core.measurement_model import MeasureModel, MeasureBlock, Cycle, MeasureBlocks

#MeasureBlocks
def test_MeasureBlock_construct():
    measure_blocks = MeasureBlocks()
    assert len(measure_blocks.blocks) == 1
    assert type(measure_blocks.blocks[0]) == MeasureBlock

def test_method_append_new():
    measure_blocks = MeasureBlocks()
    measure_blocks.append_new_block()
    assert len(measure_blocks.blocks) == 2

def test_method_append_new_cycle():
    measure_blocks = MeasureBlocks()
    measure_blocks.append_new_cycle()
    assert len(measure_blocks.cycles) == 1
    assert type(measure_blocks.cycles[0]) == Cycle

def test_method_export_standarded_blocks1():
    measure_blocks = MeasureBlocks()
    assert len(measure_blocks.export_standarded_blocks()) == 1
    assert type(measure_blocks.export_standarded_blocks()[0]) == MeasureBlock

def test_method_export_standarded_blocks2():
    measure_blocks = MeasureBlocks()
    measure_blocks.append_new_block()
    measure_blocks.append_new_cycle()
    measure_blocks.cycles[0].start_index = 0
    measure_blocks.cycles[0].stop_index = 1
    assert len(measure_blocks.export_standarded_blocks()) == 4

def test_method_export_standarded_blocks3():
    measure_blocks = MeasureBlocks()
    for _ in range(10):
        measure_blocks.append_new_block()
    for _ in range(2):
        measure_blocks.append_new_cycle()
    measure_blocks.cycles[0].start_index = 0
    measure_blocks.cycles[0].stop_index = 2
    measure_blocks.cycles[0].loop = 3

    measure_blocks.cycles[1].start_index = 5
    measure_blocks.cycles[1].stop_index = 8
    measure_blocks.cycles[1].loop = 5

    assert len(measure_blocks.export_standarded_blocks()) == 33
