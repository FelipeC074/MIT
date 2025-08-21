from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Request, APIRouter, status, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session


from app.repositories.DataBase import Get_db
from app.schemes import Schemas as S
from app.services.Email import Email_Serv

router = APIRouter(responses={status.HTTP_404_NOT_FOUND: {"message":"No Encontrado"}}) 
Service = Email_Serv()
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="portal-paciente")
templates = Jinja2Templates(directory="app/controllers/templates")


async def security_bearer(token: str = Depends(oauth2_bearer)) -> HTTPException | S.User_DB: #Funcion de barrera 
    db: Session = Depends(Get_db)
    user = Service.Bearer(token, db)
    return user                                                  #Si el usuario si existe 

@router.get("/index", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
@router.post("/portal-paciente", response_class=HTMLResponse)
def LogIn(form: OAuth2PasswordRequestForm = Depends()): 
    message = Service.LogIn(form, Depends(Get_db))
    return message #Como salida obtenemos el token, pero tambien deberia obtener HTML

@router.post("/registr/{user}", response_class=HTMLResponse)
def Registr(user: S.User_DB, request:Request):
    message = Service.Registro(user,Depends(Get_db))
    return message #Como salida obtenemos un codigo de Error o Afirmacion

#if not None == True
@router.get("/notificaciones")
def Notif(user: S.User = Depends(security_bearer)): #Aquí veremos nuestras notificaciones
    Consultas = Service.InfoUser(user, Depends(Get_db))
    return Consultas