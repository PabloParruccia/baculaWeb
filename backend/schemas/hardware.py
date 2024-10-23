from pydantic import BaseModel, EmailStr, Field, field_validator

class ServerStatus(BaseModel):
    disk: int
    cpu: int
    ram: int
    bacula: str