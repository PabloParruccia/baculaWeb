import sqlite3
from config.database import db_path



class DatosService():
    # Función para procesar el archivo de texto y extraer datos
    def process_text_file(file_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

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
                                INSERT INTO bacula (job_id, level, files, bytes, status, finished, name)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', (job_id, level, files, bytes_, status, finished, name))

            conn.commit()
        except sqlite3.Error as e:
            print(f"Error SQLite: {e}")
        except FileNotFoundError:
            print(f"Archivo no encontrado: {file_path}")
        finally:
            if conn:
                conn.close()