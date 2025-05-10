import sqlite3
from typing import Any
from contextlib import contextmanager
from sqlalchemy import create_engine
from src.database.models import Base

from ..core.data_processing import PulseBlockParam, SweepParam

# 共通のデータベース設定を定数として定義
DATABASE_NAME = "example.db"
DATABASE_URL = "sqlite:///example.db"

# コンテキストマネージャーの作成
@contextmanager
def database_connection():
    """データベース接続のコンテキストマネージャー"""
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        yield conn
    finally:
        conn.close()


def connect_database(sql: str, param: tuple = ()) -> None:
    """データベースへの接続と実行を行う"""
    with database_connection() as conn:
        conn.execute(sql, param)
        conn.commit()


def connect_database_many(sql: str, param: list[tuple]):
    """
    example.dbへexecutemanyでアクセスする

    Parameters
    ----------
    sql: str
        SQL文
    param: tuple
        SQL文に対するパラメーター
    """
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.executemany(sql, param)
        conn.commit()


def connect_database_and_get_primary_key(sql: str, param: tuple=()) -> int:
    """
    example.dbへアクセスしprimarykeyを取得する(INSERTで使用)

    Parameters
    ----------
    sql: str
        SQL文
    param: tuple
        SQL文に対するパラメーター
    """
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute(sql, param)
        last_id = cursor.lastrowid
        return last_id


def fetch_unique_data(sql: str, param: tuple = ()) -> Any:
    """単一のデータを取得する"""
    with database_connection() as conn:
        result = conn.execute(sql, param).fetchone()
        return result[0] if result else None


def fetch_all_data_record(sql: str, param: tuple=()) -> list[tuple]:
    """
    テーブルのデータをレコードごとに取得

    Parameters
    ----------
    sql: str
        抽出するSQL文
    param: tuple
        SQL文に対するパラメーター

    Returns
    -------
    result_list: list[tuple]
    """
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute(sql, param)
        rows = cursor.fetchall()

    return rows


def fetch_all_data(sql: str, param: tuple=()) -> list[Any]:
    """
    テーブルのデータをタプルを展開して1列だけ取得

    Parameters
    ----------
    sql: str
        抽出するSQL文
    param: tuple
        SQL文に対するパラメーター

    Returns
    -------
    result_list: list[Any]
        抽出結果
    """
    rows = fetch_all_data_record(sql, param)
    result_list = [row[0] for row in rows]
    return result_list


def fetch_all_data_column(sql: str, param: tuple=()) -> list[list[Any]]:
    """
    テーブルのデータをカラムごとに取得

    Returns
    -------
    result_list: list
    """
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute(sql, param)
        rows = cursor.fetchall()

        result_list = [[row[i] for row in rows] for i in range(len(rows[0]))]

    return result_list


def initialize_db() -> None:
    """
    SQLAlchemyを使用してデータベースを初期化
    """
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)


def append_record_users(user_name):
    """
    usersテーブルにデータを挿入する
    """
    sql = '''
        INSERT OR IGNORE INTO users (name) VALUES (?)
    '''
    connect_database(sql, (user_name,))


def refer_users_table():
    """
    usersテーブルのデータを参照する

    Returns
    -------
    name_list: list[str]
    """
    sql = "SELECT name from users;"
    name_list = fetch_all_data(sql)

    return name_list


def append_record_materials(material_name):
    """
    materialsテーブルにデータを挿入する
    """
    sql = '''
        INSERT OR IGNORE INTO materials (name) VALUES (?)
    '''
    connect_database(sql, (material_name,))


def refer_materials_table():
    """
    materialsテーブルのデータを参照する

    Returns
    -------
    material_list: list[str]
    """
    sql = "SELECT name from materials;"
    material_list = fetch_all_data(sql)

    return material_list


def append_record_samples(material_name, sample_name):
    """
    samplesテーブルにデータを挿入する
    """
    sql_fetch_material_id = '''
        SELECT id FROM materials WHERE name = ?
    '''
    material_id = fetch_unique_data(sql_fetch_material_id, (material_name,))

    sql_insert = '''
        INSERT OR IGNORE INTO samples (material_id, sample_name) VALUES (?, ?)
    '''
    connect_database(sql_insert, (material_id, sample_name))


def refer_samples_table(material_name) -> list[str]:
    """
    sanplesテーブルから特定の物質のsample_nameをリストで取得
    """
    sql_fetch_material_id = '''
        SELECT id FROM materials WHERE name = ?
    '''
    material_id = fetch_unique_data(sql_fetch_material_id, (material_name,))
    if material_id == None:
        return []
    
    sql_refer_samples = '''
        SELECT sample_name FROM samples WHERE material_id = ?
    '''
    sample_list = fetch_all_data(sql_refer_samples, (material_id,))
    if not type(sample_list) == list:
        return []
    
    return sample_list


def append_record_pulse_templetes(param: PulseBlockParam):
    """
    pulse_templetesテーブルにデータを挿入する
    """
    sql = '''
        INSERT OR IGNORE INTO pulse_templetes (top_voltage, top_time, base_voltage, base_time, loop, interval_time) VALUES (?, ?, ?, ?, ?, ?)
    '''
    connect_database(sql, (param.top_voltage, param.top_time, param.base_voltage, param.base_time, param.loop, param.interval_time))


def refer_pulse_templetes_table() -> list[tuple]:
    """
    pulse_templetesテーブルのデータを参照する

    Returns
    -------
    pulse_templete_list: list[tuple]
    """
    sql = "SELECT top_voltage, top_time, base_voltage, base_time, loop, interval_time FROM pulse_templetes;"
    pulse_templete_list = fetch_all_data_record(sql)

    return pulse_templete_list


def append_record_sweep_templetes(param: SweepParam):
    """
    sweep_templetesテーブルにデータを挿入する
    """
    sql = '''
        INSERT OR IGNORE INTO sweep_templetes (top_voltage, bottom_voltage, voltage_step, loop, tick_time) VALUES (?, ?, ?, ?, ?)
    '''
    connect_database(sql, (param.top_voltage, param.bottom_voltage, param.voltage_step, param.loop, param.tick_time))


def refer_sweep_templetes_table() -> list[tuple]:
    """
    sweep_templetesテーブルのデータを参照する

    Returns
    -------
    sweep_templete_list: list[tuple]
    """
    sql = "SELECT top_voltage, bottom_voltage, voltage_step, loop, tick_time FROM sweep_templetes;"
    sweep_templete_list = fetch_all_data_record(sql)

    return sweep_templete_list


# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS measurements (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         measurement_name TEXT NOT NULL,
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS measurement_history (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         datetime,
#         material_id,
#         user_id,
#         measurement_id TEXT NOT NULL,
#         param_id,
#         FOREIGN KEY (material_id) REFERENCES materials(id),
#         FOREIGN KEY (user_id) REFERENCES users(id),
#         FOREIGN KEY (measurement_id) REFERENCES measurements(id),
#         FOREIGN KEY (param_id) REFERENCES parameters(id),
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS parameters_narma (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS input_arrays (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS measured_datas_narma (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         discrete_time INTEGER,
#         min_pulse_voltage
#         max_pulse_voltage
#         train_x,
#         test_u
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS datasets_narma (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#     )
# ''')
