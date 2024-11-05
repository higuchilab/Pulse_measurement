import sqlite3

connection = sqlite3.connect("example.db")

cursor = connection.cursor()

def connect_database(sql: str, param: tuple=()):
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute(sql, param)


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
        INSERT INTO users (name)
        SELECT ?
        WHERE NOT EXISTS (SELECT 1 FROM users WHERE name = ?)
    '''
    connect_database(sql, (user_name, user_name))


def refer_users_table():
    """
    usersテーブルのデータを参照する

    Returns
    -------
    name_list: list[str]
    """
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name from users;")
        names = cursor.fetchall()

        name_list = [row[0] for row in names]

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
        INSERT INTO materials (name)
        SELECT ?
        WHERE NOT EXISTS (SELECT 1 FROM materials WHERE name = ?)
    '''
    connect_database(sql, (material_name, material_name))


def refer_materials_table():
    """
    usersテーブルのデータを参照する

    Returns
    -------
    material_list: list[str]
    """
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name from materials;")
        materials = cursor.fetchall()

        material_list = [row[0] for row in materials]

    return material_list



# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS samples (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         material_id TEXT NOT NULL,
#         sample_name TEXT NOT NULL
#     )
# ''')


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
