from ._commands import connect_database, connect_database_many, fetch_unique_data, fetch_all_data_record

def append_two_terminal_results(param: list[tuple]):
    """
    two_terminal_resultsテーブルにデータを挿入する
    """
    sql = '''
        INSERT OR IGNORE INTO two_terminal_results (history_id, elapsed_time, voltage, current) VALUES (?, ?, ?, ?)
    '''
    connect_database_many(sql, param)

