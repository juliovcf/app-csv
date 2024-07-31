import pandas as pd
import hashlib
import sqlite3

DATABASE = 'data/database.db'

def get_latest_file_hash():
    conn = sqlite3.connect(DATABASE)
    query = '''
        SELECT file_hash
        FROM avisos
        ORDER BY rowid DESC
        LIMIT 1
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    if not df.empty:
        return df['file_hash'][0]
    return None

def get_latest_upload_data(file_hash):
    conn = sqlite3.connect(DATABASE)
    query = '''
        SELECT Centro, Caja, "Cod. Estado", COUNT(*) as conteo
        FROM avisos
        WHERE file_hash = ?
        GROUP BY Centro, Caja, "Cod. Estado"
        ORDER BY conteo DESC
    '''
    df = pd.read_sql_query(query, conn, params=[file_hash])
    conn.close()
    return df.to_dict(orient='records')

def get_denegations_last_7_days():
    conn = sqlite3.connect(DATABASE)
    query = '''
        SELECT Centro, Caja, "Cod. Estado", COUNT(*) as conteo
        FROM avisos
        WHERE "Fecha /Hora" >= datetime('now', '-7 days')
        GROUP BY Centro, Caja, "Cod. Estado"
        HAVING COUNT(*) > 1
        ORDER BY conteo DESC;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        return []

    df_pivot = df.pivot_table(index=['Centro', 'Caja'], columns='Cod. Estado', values='conteo', fill_value=0).reset_index()
    df_pivot.columns.name = None  # Remove categories name

    # Convert all relevant columns to numeric
    for col in df_pivot.columns:
        if col not in ['Centro', 'Caja']:
            df_pivot[col] = pd.to_numeric(df_pivot[col], errors='coerce').fillna(0).astype(int)

    df_pivot['Total'] = df_pivot.iloc[:, 2:].sum(axis=1)  # Sum all columns except 'Centro' and 'Caja'
    return df_pivot.to_dict(orient='records')

def get_details_for_box(centro, caja):
    conn = sqlite3.connect(DATABASE)
    query = '''
        SELECT "Fecha /Hora", "Cod. Estado", "Duracion"
        FROM avisos
        WHERE Centro = ? AND Caja = ?
        ORDER BY "Fecha /Hora" DESC
    '''
    df = pd.read_sql_query(query, conn, params=[centro, caja])
    conn.close()
    return df.to_dict(orient='records')
