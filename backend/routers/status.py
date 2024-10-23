from fastapi import FastAPI, Body ,HTTPException,status,Query,Depends,File,APIRouter
from fastapi.responses import HTMLResponse,JSONResponse
import sqlite3
import subprocess
from config.database import db_path
from services.status import StatusService

route_status = APIRouter()

## filtra por el estado del back 
@route_status.get('/status/{status}', tags=['Comandos'], status_code=status.HTTP_200_OK)
async def get_people(status: str):
    result = StatusService.get_people(status)
    return result