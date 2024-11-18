import sqlite3
from typing import Any, Literal

from ..data_processing import HistoryParam, ReferHistoryParam
from ._commands import connect_database, fetch_unique_data, fetch_all_data_record

def create_measures_types_table():
    """
    measure_typesテーブルを作成
    """
    sql = '''
        CREATE TABLE IF NOT EXISTS measure_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''
    connect_database(sql)


def append_record_measure_types(name: str):
    """
    measure_typesテーブルにデータを挿入する
    """
    sql = '''
        INSERT OR IGNORE INTO measure_types (name) VALUES (?)
    '''
    connect_database(sql, (name,))


def refer_measure_types_table() -> list[tuple]:
    """
    measure_typesテーブルのデータを参照する

    Returns
    -------
    sweep_templete_list: list[tuple]
        (id, name)
    """
    sql = "SELECT id, name FROM measure_types;"
    sweep_templete_list = fetch_all_data_record(sql)

    return sweep_templete_list


def fetch_measure_type_index(measure_type: Literal["NARMA", "2-terminate I-Vsweep", "2-terminate Pulse"]) -> int:
    sql_fetch_material_id = '''
        SELECT id FROM measure_types WHERE name = ?
    '''
    id = fetch_unique_data(sql_fetch_material_id, (measure_type,))
    return id



def create_history_table():
    """
    historyテーブルを作成
    """
    sql = '''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            sample_id INTEGER NOT NULL,
            measure_type_id INTEGER NOT NULL,
            option TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (sample_id) REFERENCES samples(id),
            FOREIGN KEY (measure_type_id) REFERENCES measures(id)
        )
    '''
    connect_database(sql)


def append_record_history(param: HistoryParam):
    """
    historyテーブルにデータを挿入する
    """

    sql_fetch_user_id = '''
        SELECT id FROM users WHERE name = ?
    '''
    user_id = fetch_unique_data(sql_fetch_user_id, (param.user_name,))

    sql_fetch_sample_id = '''
        SELECT id FROM samples WHERE name = ?
    '''
    sample_id = fetch_unique_data(sql_fetch_sample_id, (param.sample_name,))

    sql_fetch_measure_type_id = '''
        SELECT id FROM measure_types WHERE name = ?
    '''
    measure_type_id = fetch_unique_data(sql_fetch_measure_type_id, (param.measure_type,))

    sql_insert = '''
        INSERT OR IGNORE INTO history (user_id, sample_id, measure_type_id, option) VALUES (?, ?, ?, ?)
    '''
    connect_database(sql_insert, (user_id, sample_id, measure_type_id, param.option))


def refer_history_table(param: ReferHistoryParam) -> list[tuple]:
    """
    historyテーブルのデータを参照する

    Returns
    -------
    history: list[tuple]
    """
    query = '''
        SELECT 
            history.created_at,
            users.name,
            materials.name,
            samples.sample_name,
            measure_types.name,
            history.option
        FROM 
            history
        LEFT JOIN
            users ON history.user_id = users.id
        LEFT JOIN
            samples ON history.sample_id = samples.id
        LEFT JOIN
            measure_types ON history.measure_type_id = measure_types.id
        LEFT JOIN
            materials ON samples.material_id = materials.id
        WHERE 1=1
    '''
    params = []

    if param.operator:
        query += " AND users.name = ?"
        params.append(param.operator)

    if param.material:
        query += " AND materials.name = ?"
        params.append(param.material)

    if param.sample:
        query += " AND samples.sample_name = ?"
        params.append(param.sample)

    if param.measure_type:
        query += " AND measure_types.name = ?"
        params.append(param.measure_type)

      
        
    history = fetch_all_data_record(query, tuple(params))

    return history

