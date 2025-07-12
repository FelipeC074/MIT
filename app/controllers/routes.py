from fastapi import FastAPI, Request, APIRouter, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(responses={status.HTTP_404_NOT_FOUND: {"message":"No Encontrado"}})

# Carga las plantillas desde la carpeta "templates"
templates = Jinja2Templates(directory="app/controllers/templates")

@router.get("/")
async def Indexium():
    return {"Heero":"hello"}

@router.get("/index", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})