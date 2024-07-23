import sqlite3

# Ruta de la base de datos SQLite
db_path = '/media/parrucciape/fb97eb58-e727-4ca4-8cb4-44340e5f25bf/proyectoBacula/cds/sqlite.sql'

# Crear y conectar a la base de datos SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear la tabla terminated_jobs
cursor.execute('''
CREATE TABLE IF NOT EXISTS terminated_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    level TEXT,
    files INTEGER,
    bytes TEXT,
    status TEXT,
    finished TEXT,
    name TEXT
)
''')

# Función para procesar el archivo de texto y extraer datos
def process_text_file(file_path):
    with open(file_path, 'r') as file:
        server_name = None
        for line in file:
            line = line.strip()
            if line.startswith('-------- BACKUP DE'):
                server_name = line.split('-------- BACKUP DE ')[1].strip()
            elif line and not line.startswith('=') and not line.startswith('JobId') and not line.startswith('You have messages') and not line.startswith('exit'):
                parts = line.split()
                if len(parts) == 9:
                    job_id, level, files, bytes_, status, finished_date, finished_time, *name_parts = parts
                    name = ' '.join(name_parts)
                    finished = f"{finished_date} {finished_time}"
                    cursor.execute('''
                        INSERT INTO terminated_jobs (job_id, level, files, bytes, status, finished, name)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (job_id, level, files, bytes_, status, finished, name))

# Procesar el archivo de texto
process_text_file('backup_data.txt')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
