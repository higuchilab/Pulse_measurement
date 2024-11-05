import pyvisa as visa

VISA_DLL_PATH = r'C:\WINDOWS\system32\visa64.dll'
GPIB_ADDRESS = 'GPIB1::1::INSTR'
DEVICE_TIMEOUT = 5000

# デバイスの初期化
def device_connection(visa_dll_path, gpib_address: str):
    try:
        rm = visa.ResourceManager(VISA_DLL_PATH)
        dev = rm.open_resource(GPIB_ADDRESS)
        dev.timeout = DEVICE_TIMEOUT
    except:
        print('Caution: visa is stoped')

    return dev

def write_command(command: str, dev) -> None:
    """デバイスにコマンドを送信します。"""
    dev.write(command)

def prepare_device(dev) -> None:
    """測定装置の準備を行います。"""
    start_commands = [
        "*RST",  # 初期化
        "M1",    # トリガーモード HOLD
        "OH1",   # ヘッダON
        "VF",    # 電圧発生
        "F2",    # 電流測定
        "MD0",   # DCモード
        "R0",    # オートレンジ
        "OPR"    # 出力
    ]
    for command in start_commands:
        try:
            write_command(command, dev)
        except Exception as e:
            print(f"コマンド '{command}' の実行中にエラーが発生しました: {e}")

