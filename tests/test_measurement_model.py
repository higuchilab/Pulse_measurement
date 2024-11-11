import pytest
import numpy as np
from src.core.measurement_model import MeasureModel, MeasureBlocks

class TestMeasureModel:
    @pytest.fixture
    def measure_blocks(self):
        return MeasureBlocks()
    
    @pytest.fixture
    def measure_model(self, measure_blocks):
        return MeasureModel(measure_blocks)

    def test_make_measure_list_basic(self, measure_model):
        # 基本的なブロックを追加してテスト
        measure_model.blocks.append_new_block(
            loop=2,
            V_top=1.0,
            V_base=0.0,
            top_time=2.0,
            base_time=2.0,
            interval=1.0
        )
        
        # tick = 0.1の場合、各時間は以下のポイント数になる
        # base_time (2.0s) = 20 points
        # top_time (2.0s) = 20 points
        # interval (1.0s) = 10 points
        # 合計 = (20 + 20 + 10) * 2 loops = 100 points
        
        result = measure_model.input_V_list
        expected_length = 100
        assert len(result) == expected_length
        
        # 値の検証
        assert result[0] == 0.0  # base voltage
        assert result[20] == 1.0  # top voltage
        assert result[40] == 0.0  # interval voltage

    def test_make_measure_list_with_cycle(self, measure_model):
        # ブロックを追加
        measure_model.blocks.append_new_block(
            loop=1,
            V_top=1.0,
            V_base=0.0,
            top_time=1.0,
            base_time=1.0,
            interval=1.0
        )
        
        # サイクルを追加
        measure_model.blocks.append_new_cycle()
        measure_model.blocks.cycles[0].start_index = 0
        measure_model.blocks.cycles[0].stop_index = 0
        measure_model.blocks.cycles[0].loop = 2
        
        result = measure_model.input_V_list
        # 1ブロックあたり (10 + 10 + 10) = 30 points
        # サイクルループ2回で 30 * 2 = 60 points
        expected_length = 60
        assert len(result) == expected_length

    def test_make_model_from_narma_input_array(self, measure_model):
        input_array = np.array([0.5, 1.0, 1.5])
        pulse_width = 1.0
        off_width = 1.0
        tick = 0.1
        base_voltage = 0.0
        
        measure_model.make_model_from_narma_input_array(
            pulse_width=pulse_width,
            off_width=off_width,
            tick=tick,
            base_voltage=base_voltage,
            input_array=input_array
        )
        
        # 検証
        assert measure_model.tick == tick
        assert len(measure_model.blocks.blocks) == len(input_array)
        
        # 各ブロックの設定を確認
        for i, block in enumerate(measure_model.blocks.blocks):
            assert block.V_top == input_array[i]
            assert block.V_base == base_voltage
            assert block.top_time == pulse_width
            assert block.base_time == off_width
            assert block.interval == 0.0
            assert block.loop == 1
        
        # input_V_listの長さを確認
        result = measure_model.input_V_list
        points_per_block = int((pulse_width + off_width) / tick)
        expected_length = points_per_block * len(input_array)
        assert len(result) == expected_length 