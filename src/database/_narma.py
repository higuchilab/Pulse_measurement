from ._commands import connect_database, connect_database_and_get_primary_key, fetch_unique_data, fetch_all_data_record, connect_database_many

def create_narma_templetes_table():
    """
    narma_templetesテーブルを作成
    """
    sql = '''
        CREATE TABLE IF NOT EXISTS narma_templetes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tot_discrete_time INTEGER NOT NULL,
            top_voltage REAL NOT NULL,
            bottom_voltage REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (tot_discrete_time, top_voltage, bottom_voltage)
    '''
    connect_database(sql)


def append_record_narma_templetes(param: tuple):
    """
    narma_templetesテーブルにデータを挿入する
    """
    sql = '''
        INSERT OR IGNORE INTO pulse_templetes (tot_discrete_time, top_voltage, bottom_voltage) VALUES (?, ?, ?)
    '''
    return connect_database_and_get_primary_key(sql, param)


def create_narma_input_array():
    """
    narma_input_arrayテーブルを作成
    """
    sql = '''
        CREATE TABLE IF NOT EXISTS narma_input_array (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            narma_templete_id INTEGER NOT NULL,
            discrete_time INTEGER NOT NULL,
            input_voltage REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (narma_templete_id) REFERENCES narma_templetes(id)
    '''
    connect_database(sql)


def append_narma_input_array(param: list[tuple]):
    """
    narma_input_arrayテーブルにデータを挿入する
    """
    sql = '''
        INSERT OR IGNORE INTO narma_input_array (narma_templete_id, discrete_time, input_voltage) VALUES (?, ?, ?)
    '''
    connect_database_many(sql, param)
