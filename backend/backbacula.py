from fastapi import FastAPI, Body ,HTTPException,status,Query,Depends,File
from fastapi.responses import HTMLResponse
from typing import Annotated , Any,Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import secrets
import psutil
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import subprocess
from fastapi import UploadFile
import os
import shutil
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel,field_validator,Field
import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
from fastapi.templating import Jinja2Templates
from routers.cliente import route_cliente


#database
#from database.database import Base,engine,Session
#from models.movie import Movie as MovieModel

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"

origins = [
    "http://127.0.0.1:5500",  # Origen de tu HTML
    "http://localhost:5500",  # Origen de tu HTML (alternativo)
]
##midleware para permitir conexiones con el back
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db_path = '/media/parrucciape/fb97eb58-e727-4ca4-8cb4-44340e5f25bf/proyectoBacula/cds/backend.db'



@app.get('/', tags=['home'])
def message():
    return HTMLResponse('BACULA BACKUP')

##muestra todo el back
@app.get("/reporte")
async def get_people():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bacula")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener personas: {str(e)}")
## filtra por nombre de cliente bacula

@app.get('/nameclient/{name}')
async def get_people(name: str):
     conn = sqlite3.connect(db_path)
     cursor = conn.cursor()
     cursor.execute("SELECT * FROM bacula WHERE Name = ?", (name,))
     person_data = cursor.fetchone()
     conn.close()
     if person_data:
         return {'JobId': person_data[0], 'Level': person_data[1], 'Files': person_data[2], 'Bytes': person_data[3], 'Status': person_data[4], 'Finished': person_data[5], 'Name': person_data[6]}
     else:
        raise HTTPException(status_code=404, detail='Person not found')
## filtra por el estado del back 
@app.get('/status/{status}')
async def get_people(status: str):
     conn = sqlite3.connect(db_path)
     cursor = conn.cursor()
     cursor.execute("SELECT * FROM bacula WHERE Status = ?", (status,))
     person_data = cursor.fetchone()
     conn.close()
     if person_data:
         return {'JobId': person_data[0], 'Level': person_data[1], 'Files': person_data[2], 'Bytes': person_data[3], 'Status': person_data[4], 'Finished': person_data[5], 'Name': person_data[6]}
     else:
        raise HTTPException(status_code=404, detail='Person not found')

##filtra por el tiempo y hora de finalizacion
@app.get('/finished/{finished}')
async def get_people(finished: str):
     conn = sqlite3.connect(db_path)
     cursor = conn.cursor()
     cursor.execute("SELECT * FROM bacula WHERE Finished = ?", (finished,))
     person_data = cursor.fetchone()
     conn.close()
     if person_data:
         return {'JobId': person_data[0], 'Level': person_data[1], 'Files': person_data[2], 'Bytes': person_data[3], 'Status': person_data[4], 'Finished': person_data[5], 'Name': person_data[6]}
     else:
        raise HTTPException(status_code=404, detail='Person not found')
     #########################




# ## obtiene todos los datos de la tabla BACULA
# @app.get('/reportes')
# async def get_reportes():
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM bacula")
#     reportes = cursor.fetchall()
#     conn.close()
#     return reportes
 
# ## filtro para traer datos de un nombre en especifico
# @app.get('/reportes/{cliente}')
# async def get_reportes_por_cliente(cliente: str):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM bacula WHERE Name = ?", (cliente,))
#     reportes = cursor.fetchall()
#     conn.close()
#     return reportes

# ##Elimina los registros duplicados de los resultados, devolviendo solo valores únicos.
# @app.get('/nameclient')
# async def get_clients():
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute("SELECT DISTINCT Name FROM bacula")
#     clients = [row[0] for row in cursor.fetchall()]
#     conn.close()
#     return clients

###########################################
#comandos para ejecutar backup y mensagges#
###########################################

@app.post("/bconsole")
async def ejecutar_script_bconsole():
    try:
        # Ruta al script .sh
        ruta_script = "/media/parrucciape/fb97eb58-e727-4ca4-8cb4-44340e5f25bf/proyectoBacula/cds/bconsole.sh"
        # Ejecutar el script
        proceso = subprocess.run(["sh", ruta_script], capture_output=True)
        # Verificar el resultado y retornar la salida o un mensaje de error
        if proceso.returncode == 0:
            return {"salida": proceso.stdout.decode("utf-8")}
        else:
            return {"error": proceso.stderr.decode("utf-8")}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/bconsole2")
async def ejecutar_script_bconsole():
    try:
        # Ruta al script .sh
        ruta_script = "/media/parrucciape/fb97eb58-e727-4ca4-8cb4-44340e5f25bf/proyectoBacula/cds/bconsole2.sh"
        # Ejecutar el script
        proceso = subprocess.run(["sh", ruta_script], capture_output=True)
        # Verificar el resultado y retornar la salida o un mensaje de error
        if proceso.returncode == 0:
            return {"salida": proceso.stdout.decode("utf-8")}
        else:
            return {"error": proceso.stderr.decode("utf-8")}
    except Exception as e:
        return {"error": str(e)}

##########################################
# estado del hardware de mi servidor bacula#
##########################################
class ServerStatus(BaseModel):
    disk: int
    cpu: int
    ram: int
    bacula: str

def check_service_status(service_name: str) -> str:
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', service_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return "activo"
        else:
            return "inactivo"
    except Exception as e:
        return f"error: {e}"

def check_service_status(service_name: str) -> str:
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', service_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return "activo"
        else:
            return "inactivo"
    except Exception as e:
        return f"error: {e}"

@app.get("/server-status", response_model=ServerStatus)
def get_server_status():
    # Obtén el uso del disco
    disk_usage = psutil.disk_usage('/')
    disk_percent = disk_usage.percent

    # Obtén el uso de la CPU
    cpu_usage = psutil.cpu_percent(interval=1)

    # Obtén el uso de la RAM
    ram_usage = psutil.virtual_memory().percent

    # Verifica el estado del servicio Bacula
    bacula_status = check_service_status('bacula-fd')

    print(f"Disk usage: {disk_usage}, CPU usage: {cpu_usage}%, RAM usage: {ram_usage}%")

    return ServerStatus(
        disk=int(disk_percent),
        cpu=int(cpu_usage),
        ram=int(ram_usage),
        bacula=bacula_status
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)




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
                    if len(parts) >= 8:
                        job_id = parts[0]
                        level = parts[1]
                        files = parts[2]
                        
                        # Verificar si bytes tiene una unidad
                        if parts[3]=='0' or 'OK' in parts[4] or 'Error' in parts[4]:
                            bytes_ = parts[3]
                            status = parts[4]
                            finished_date = parts[5]
                            finished_time = parts[6]
                            name = ' '.join(parts[7:])
                        else:


                            bytes_ = parts[3] + ' ' + parts[4]
                            status = parts[5]
                            finished_date = parts[6]
                            finished_time = parts[7]
                            name = ' '.join(parts[8:])
                            
                        finished = f"{finished_date} {finished_time} "
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


# Ruta para importar los datos
@app.post("/importar_datos")
def importar_datos():
    file_path = '/media/parrucciape/fb97eb58-e727-4ca4-8cb4-44340e5f25bf/proyectoBacula/cds/backup_data.txt'  # Ajusta la ruta al archivo de texto
    process_text_file(file_path)
    return {"message": "Datos importados correctamente"}










