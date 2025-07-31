from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Literal
from fastapi import FastAPI, Request, APIRouter, status, Depends, Query, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from repositories.DataBase import Get_db
from schemes import Schemas as S
from repositories.Repo import Repositorio

router = APIRouter(responses={status.HTTP_404_NOT_FOUND: {"message":"No Encontrado"}}) 

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="login")
# Carga las plantillas desde la carpeta "templates"
templates = Jinja2Templates(directory="app/controllers/templates")

@router.get("/index", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
#token: str = Depends(oauth2_bearer)
@router.post("/login")
def LogIn(form: OAuth2PasswordRequestForm = Depends()):
    pass

@router.post("/registr")
def Registr():
    pass