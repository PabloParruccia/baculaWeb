from fastapi import FastAPI, Body ,HTTPException,status,Query,Depends,File,APIRouter
from fastapi.responses import HTMLResponse,JSONResponse
import sqlite3
from config.database import db_path
from services.datos import DatosService
route_datos = APIRouter()


# Ruta para importar los datos
@route_datos.post("/importar_datos", tags=['ImportDatos'], status_code=status.HTTP_200_OK)
def importar_datos():
    file_path = '/media/parrucciape/fb97eb58-e727-4ca4-8cb4-44340e5f25bf/proyectoBacula/cds/backup_data.txt'  # Ajusta la ruta al archivo de texto
    DatosService.process_text_file(file_path)
    return {"message": "Datos importados correctamente"}