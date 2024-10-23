from fastapi import FastAPI, Body ,HTTPException,status,Query,Depends,File,APIRouter
from fastapi.responses import HTMLResponse,JSONResponse

import subprocess
from config.database import db_path

route_comandos = APIRouter()
###########################################
#comandos para ejecutar backup y mensagges#
###########################################

@route_comandos.post("/bconsole", tags=['Comandos'], status_code=status.HTTP_200_OK)
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
    
@route_comandos.post("/bconsole2", tags=['Comandos'], status_code=status.HTTP_200_OK)
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
