from pydantic import BaseModel, ConfigDict
from enum import Enum

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: str

class User_DB(User):
    password: str

class Consulta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    horario: str # Time
    user: str
    
class ConfirmResponse(str, Enum):
    Positivo = "Funciono Correctamente"
    Negativo = "Ha hecho algo mal"
    ErrorServ = "Error del Servidor"
