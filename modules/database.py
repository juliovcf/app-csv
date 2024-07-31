import sqlite3
import pandas as pd

DATABASE = 'data/database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS avisos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Centro TEXT,
        Caja TEXT,
        "Fecha /Hora" TIMESTAMP,
        "Cod. Estado" INTEGER,
        Duracion TEXT,
        file_hash TEXT
    )
    ''')
    conn.commit()
    conn.close()

def save_to_db(df, file_hash):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Renombrar la columna 'Duración' a 'Duracion'
    df.rename(columns={'Duración': 'Duracion'}, inplace=True)
    
    for index, row in df.iterrows():
        # Convertir valores a string
        centro = str(row['Centro']) if pd.notnull(row['Centro']) else None
        caja = str(row['Caja']) if pd.notnull(row['Caja']) else None
        fecha_hora = row['Fecha /Hora'].strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(row['Fecha /Hora']) else None
        cod_estado = row['Cod. Estado'] if pd.notnull(row['Cod. Estado']) else None
        duracion = str(row['Duracion']) if pd.notnull(row['Duracion']) else None

        # Debugging output
        print(f"Inserting row: Centro={centro}, Caja={caja}, Fecha /Hora={fecha_hora}, Cod. Estado={cod_estado}, Duracion={duracion}, file_hash={file_hash}")

        try:
            cursor.execute('''
            INSERT INTO avisos (Centro, Caja, "Fecha /Hora", "Cod. Estado", Duracion, file_hash)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (centro, caja, fecha_hora, cod_estado, duracion, file_hash))
        except sqlite3.InterfaceError as e:
            print(f"Error inserting row: {e}")
            print(f"Centro={type(centro)}, Caja={type(caja)}, Fecha /Hora={type(fecha_hora)}, Cod. Estado={type(cod_estado)}, Duracion={type(duracion)}, file_hash={type(file_hash)}")
            raise e
    conn.commit()
    conn.close()

def check_file_hash_exists(file_hash):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM avisos WHERE file_hash = ?', (file_hash,))
    result = cursor.fetchone()[0]
    conn.close()
    return result > 0
