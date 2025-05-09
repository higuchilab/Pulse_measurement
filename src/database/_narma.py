from ._commands import connect_database, connect_database_and_get_primary_key, fetch_unique_data, fetch_all_data_record, connect_database_many


def append_record_narma_templetes(param: tuple):
    """
    narma_templetesテーブルにデータを挿入する
    """
    sql = '''
        INSERT OR IGNORE INTO narma_templetes (tot_discrete_time, top_voltage, bottom_voltage) VALUES (?, ?, ?)
    '''
    return connect_database_and_get_primary_key(sql, param)


def append_narma_input_array(param: list[tuple]):
    """
    narma_input_arrayテーブルにデータを挿入する
    """
    sql = '''
        INSERT OR IGNORE INTO narma_input_array (narma_templete_id, discrete_time, input_voltage) VALUES (?, ?, ?)
    '''
    connect_database_many(sql, param)
