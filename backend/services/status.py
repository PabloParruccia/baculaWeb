from fastapi import FastAPI, Body ,HTTPException,status,Query,Depends,File,APIRouter
from fastapi.responses import HTMLResponse,JSONResponse
import sqlite3
from config.database import db_path




class StatusService():
    async def get_people(status: str):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM terminated_jobs WHERE Status = ?", (status,))
        person_data = cursor.fetchone()
        conn.close()
        if person_data:
            return {'JobId': person_data[0], 'Level': person_data[1], 'Files': person_data[2], 'Bytes': person_data[3], 'Status': person_data[4], 'Finished': person_data[5], 'Name': person_data[6]}
        else:
            raise HTTPException(status_code=404, detail='Person not found')