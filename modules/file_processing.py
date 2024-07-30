import pandas as pd
import hashlib

def process_file(file):
    df = pd.read_csv(file, encoding='latin1', delimiter=';', on_bad_lines='skip')
    relevant_columns = ['Centro', 'Caja', 'Fecha /Hora', 'Cod. Estado']
    df = df[relevant_columns]
    df['Fecha /Hora'] = pd.to_datetime(df['Fecha /Hora'], format='%d/%m/%Y %H:%M:%S')
    return df

def calculate_file_hash(file):
    file.seek(0)  # Ensure we're at the start of the file
    hasher = hashlib.sha256()
    buf = file.read(8192)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(8192)
    file.seek(0)  # Reset the file pointer to the beginning
    return hasher.hexdigest()
