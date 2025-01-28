from ._commands import connect_database, connect_database_many, fetch_unique_data, fetch_all_data_record

def create_two_terminal_results_table():
    """
    two_terminal_resultsテーブルを作成
    """
    sql = '''
        CREATE TABLE IF NOT EXISTS two_terminal_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            history_id INTEGER NOT NULL,
            elapsed_time REAL,
            voltage REAL,
            current REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (history_id) REFERENCES history(id)
        )
    '''
    connect_database(sql)


def append_two_terminal_results(param: list[tuple]):
    """
    two_terminal_resultsテーブルにデータを挿入する
    """
    sql = '''
        INSERT OR IGNORE INTO two_terminal_results (history_id, elapsed_time, voltage, current) VALUES (?, ?, ?, ?)
    '''
    connect_database_many(sql, param)


def create_four_terminal_results_table():
    """
    four_terminal_resultsテーブルを作成
    """
    sql = '''
        CREATE TABLE IF NOT EXISTS four_terminal_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            history_id INTEGER NOT NULL,
            elapsed_time REAL,
            voltage_1 REAL,
            current_1 REAL,
            voltage_2 REAL,
            current_2 REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (history_id) REFERENCES history(id)
        )
    '''
    connect_database(sql)
