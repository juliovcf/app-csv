import sqlite3

DATABASE = 'data/database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avisos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Centro TEXT,
            Caja TEXT,
            "Fecha /Hora" TEXT,
            "Cod. Estado" INTEGER,
            Estado TEXT,
            file_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(df, file_hash):
    conn = sqlite3.connect(DATABASE)
    df['file_hash'] = file_hash
    df.to_sql('avisos', conn, if_exists='append', index=False)
    conn.close()

def check_file_hash_exists(file_hash):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM avisos WHERE file_hash = ?', (file_hash,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
