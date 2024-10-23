from fastapi import FastAPI, Body ,HTTPException,status,Query,Depends,File,APIRouter
from fastapi.responses import HTMLResponse,JSONResponse
import sqlite3
import subprocess
from config.database import db_path


class UsuarioService():
    
    def __init__(self, db) -> None:
        self.db = db

    def get_usuarios():
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM terminated_jobs")
            rows = cursor.fetchall()
            conn.close()
            return rows
        
        

    def asd(cliente):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM terminated_jobs WHERE Name = ?", (cliente,))
        result = cursor.fetchall()
        conn.close()
        return result


    def get_usuarios_name(name):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM terminated_jobs WHERE Name = ?", (name,))
        person_data = cursor.fetchone()
        conn.close()
        if person_data:
            return {'JobId': person_data[0], 'Level': person_data[1], 'Files': person_data[2], 'Bytes': person_data[3], 'Status': person_data[4], 'Finished': person_data[5], 'Name': person_data[6]}
        else:
            raise HTTPException(status_code=404, detail='Person not found')
        

#     def get_usuarios_by_correo(self, correo):
#         result = self.db.query(UsuarioModel).filter(UsuarioModel.correo == correo).first()
#         return result

#     def create_usuarios(self, usuario: UsuarioOut):
#         new_usuario = UsuarioModel(**usuario.dict())
#         self.db.add(new_usuario)
#         self.db.commit()
#         return
# #   def update_movie(self, id: int, data: Movie):
# #         movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
# #         movie.title = data.title
# #         movie.overview = data.overview
# #         movie.year = data.year
# #         movie.rating = data.rating
# #         movie.category = data.category
# #         self.db.commit()
# #         return

#     def update_usuarios(self, id: int, data: UsuarioOut):
#         dbusuario = self.db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
#         dbusuario.apellido = data.apellido
#         dbusuario.nombre = data.nombre
#         dbusuario.correo = data.correo
#         dbusuario.pais = data.pais
#         dbusuario.cuidad = data.cuidad
#         dbusuario.direccion = data.direccion
#         dbusuario.telefono = data.telefono
#         dbusuario.rol = data.rol
#         dbusuario.hashed_password = data.hashed_password
#         self.db.commit()
#         return dbusuario

#     def delete_usuarios(self, id: int):
#        self.db.query(UsuarioModel).filter(UsuarioModel.id == id).delete()
#        self.db.commit()
#        return