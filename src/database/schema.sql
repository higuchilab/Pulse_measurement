CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER NOT NULL,
    sample_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (material_id) REFERENCES materials(id),
    UNIQUE (material_id, sample_name)
);

CREATE TABLE IF NOT EXISTS pulse_templetes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    top_voltage REAL NOT NULL,
    top_time REAL NOT NULL CHECK(top_time >= 0),
    base_voltage REAL NOT NULL,
    base_time REAL NOT NULL CHECK(base_time >= 0),
    loop INTEGER NOT NULL CHECK(loop > 0),
    interval_time REAL NOT NULL CHECK(interval_time >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (top_voltage, top_time, base_voltage, base_time, loop, interval_time)
);

CREATE TABLE IF NOT EXISTS sweep_templetes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    top_voltage REAL NOT NULL,
    bottom_voltage REAL NOT NULL,
    voltage_step REAL NOT NULL CHECK(voltage_step > 0),
    loop INTEGER NOT NULL CHECK(loop > 0),
    tick_time REAL NOT NULL CHECK(tick_time >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (top_voltage, bottom_voltage, voltage_step, loop, tick_time)
);

CREATE TABLE IF NOT EXISTS measure_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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
);

CREATE TABLE IF NOT EXISTS two_terminal_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    history_id INTEGER NOT NULL,
    elapsed_time REAL,
    voltage REAL,
    current REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (history_id) REFERENCES history(id)
);

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
);

CREATE TABLE IF NOT EXISTS narma_templetes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tot_discrete_time INTEGER NOT NULL,
    top_voltage REAL NOT NULL,
    bottom_voltage REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (tot_discrete_time, top_voltage, bottom_voltage)
);

CREATE TABLE IF NOT EXISTS narma_input_array (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    narma_templete_id INTEGER NOT NULL,
    discrete_time INTEGER NOT NULL,
    input_voltage REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (narma_templete_id) REFERENCES narma_templetes(id)
);
