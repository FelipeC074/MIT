from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Request, APIRouter, status, Depends, HTTPException, Cookie 
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session

from app.repositories.DataBase import Get_db
from app.schemes import Schemas as S
from app.services.Email import Email_Serv

router = APIRouter(responses={status.HTTP_404_NOT_FOUND: {"message":"No Encontrado"}}) 
Service = Email_Serv()
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="portal-paciente.html")
templates = Jinja2Templates(directory="app/controllers/templates")

#: str = Depends(oauth2_bearer)
def security_bearer(request: Request, db: Session = Depends(Get_db)) -> HTTPException | S.User_DB: #Funcion de barrera 
    token = request.cookies.get("access_token")  #Obtenemos el token de las cookies
    if not token:
        return None
    
    scheme, _, param = token.partition(" ")
    if not param or scheme.lower() != "bearer": #Si scheme no es Bearer o no hay param
        return None
    #Hay param y scheme es Bearer
    user = Service.Bearer(param, db)
    return user                                                  #Si el usuario si existe 

@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/contacto.html", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("contacto.html", {"request": request})

@router.get("/laboratorio.hmtl", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("laboratorio.html", {"request": request})

@router.get("/profesionales.html", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("profesionales.html", {"request": request})

@router.get("/servicios.html", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("servicios.html", {"request": request})

@router.get("/portal-paciente.html", response_class=HTMLResponse)
def get_login(request: Request):
    return templates.TemplateResponse("portal-paciente.html", {"request": request})

@router.get("/servicio.html", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("servicio.html", {"request": request})

@router.post("/portal-paciente.html", response_class=HTMLResponse)
def LogIn(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(Get_db)):
    message = Service.LogIn(form, db) #El email no se usa en el login 
  
    if isinstance(message, HTTPException):
        raise message
    
    response = RedirectResponse(url="/info-paciente.html/", status_code=status.HTTP_303_SEE_OTHER)#Parte HTML de la respuesta
    # Aquí se establece la cookie con el token JWT
    response.set_cookie(
        key="access_token",
        value=f"Bearer {message["access_token"]}",
        max_age=3600  # La cookie expirará en 1 hora (3600 segundos)
        #httponly=True,  # No accesible a través de JavaScript
        #secure=True,    # Solo se envía con HTTPS
        #samesite="Lax"  # Restringe el envío de la cookie en solicitudes de terceros 
    )
    return response #Como salida obtenemos el token(Cookie), pero tambien HTML

@router.get("/registr.html", response_class=HTMLResponse)
def get_registr(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
#felipecarando11@gmail.com
@router.post("/registr.html", response_class=HTMLResponse)
def Registr(user: S.User_DB, request:Request, db: Session = Depends(Get_db)):
    message = Service.Registro(user, db)
    if isinstance(message, HTTPException):
        raise message
    return templates.TemplateResponse("index.html", {"request": request}) #Agregar mensaje de éxito

#if not None == True
@router.get("/info-paciente.html/", response_class=HTMLResponse)
def Notif(user: S.User_DB = Depends(security_bearer), db: Session = Depends(Get_db)): #Aquí veremos nuestras notificaciones
    Consultas = Service.InfoUser(user, db) #Trae todos los datos de las consultas del usuario
    return Consultas