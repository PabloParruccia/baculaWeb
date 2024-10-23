from fastapi import FastAPI, Body ,HTTPException,status,Query,Depends,File,APIRouter
from fastapi.responses import HTMLResponse,JSONResponse

from services.finished import FinishedService

route_finished = APIRouter()

##filtra por el tiempo y hora de finalizacion
@route_finished.get('/finished/{finished}', tags=['Comandos'], status_code=status.HTTP_200_OK)
async def get_people(finished: str):
    result = FinishedService.get_people(finished)
    return result
     #########################
