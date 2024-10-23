from fastapi import FastAPI, Body ,HTTPException,status,Query,Depends,File,APIRouter
from fastapi.responses import HTMLResponse,JSONResponse
import sqlite3
import subprocess
from config.database import db_path
from services.clientes import UsuarioService
route_cliente = APIRouter()


# ## obtiene todos los datos de la tabla BACULA
# @route_cliente.get('/reportes', tags=['Datos'], status_code=status.HTTP_200_OK)
# async def get_reportes():
#     retorte = UsuarioService.get_usuarios()
#     return retorte
 
# ## filtro para traer datos de un nombre en especifico
# @route_cliente.get('/reportes/{cliente}', tags=['usuarios'], status_code=status.HTTP_200_OK)
# async def get_reportes_por_cliente(cliente: str):
#     reportes= UsuarioService.get_usuarios_name(cliente)
#     return reportes

# ##Elimina los registros duplicados de los resultados, devolviendo solo valores únicos.
# @route_cliente.get('/nameclient', tags=['usuarios'], status_code=status.HTTP_200_OK)
# async def get_clients():
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute("SELECT DISTINCT Name FROM terminated_jobs")
#     clients = [row[0] for row in cursor.fetchall()]
#     conn.close()
#     return clients

@route_cliente.get('/nameclient/{name}', tags=['usuarios'], status_code=status.HTTP_200_OK)
async def get_people(name: str):
    reportes= UsuarioService.get_people_name(name)
    return reportes
     
     ##muestra todo el back
@route_cliente.get("/reporte", tags=['Datos'], status_code=status.HTTP_200_OK)
async def get_people():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM terminated_jobs")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener personas: {str(e)}")
## filtra por nombre de cliente bacula
