import sqlite3
from typing import Any

connection = sqlite3.connect("example.db")

cursor = connection.cursor()

def connect_database(sql: str, param: tuple=()):
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute(sql, param)


def fetch_unique_data(sql: str, param: tuple=()) -> Any:
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute(sql, param)
        result = cursor.fetchone()
        if result == None:
            return None
        
        return result[0]


def fetch_all_data(sql: str, param: tuple=()) -> list:
    """
    テーブルのデータを取得

    Returns
    -------
    result_list: list
    """
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute(sql, param)
        rows = cursor.fetchall()

        result_list = [row[0] for row in rows]

    return result_list


def create_users_table():
    sql = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''
    connect_database(sql)


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
    

def create_materials_table():
    sql = '''
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''
    connect_database(sql)


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


def create_samples_table():
    """
    samplesテーブルを作成
    """
    sql = '''
        CREATE TABLE IF NOT EXISTS samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER NOT NULL,
            sample_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (material_id) REFERENCES materials(id),
            UNIQUE (material_id, sample_name)
        )
    '''
    connect_database(sql)


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


def refer_samples_table(material_name):
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
