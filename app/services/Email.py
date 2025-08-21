from email_validator import validate_email, EmailNotValidError
from smtplib import SMTP_SSL
from email.message import EmailMessage
from app.schemes import Schemas as S
from app.repositories.Repo import Repositorio
import pandas as pd
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import jwt, JWTError

import os
from dotenv import load_dotenv

load_dotenv()
passwordE = os.getenv("password")
SECRET = os.getenv("SECRET")
crypt = CryptContext(schemas=["bcrypt"])

class Email_Serv(): 
    def __init__(self, email, password, Repo):
        __email = "mit.prueba@hotmail.com"
        __password = passwordE
        self.Repo = Repositorio()
    
    def Notificacion(self, user: S.User, message: str): #Envia una notificacion a un Usuario
        Notificacc = EmailMessage()
        Notificacc["Subject"] = "MIT" 
        Notificacc["From"] = self.email 
        Notificacc["Subject"] = user.email
        Notificacc.set_content = message
        with SMTP_SSL("smtp.gmail.com") as conn:
          conn.login(self.email, passwordE)
          conn.send_message(Notificacc)

    def ValEmail(self, email:str) -> bool:
        """
        Chequea si un string es un correo, que existe y se le puedan mandar mensajes
        """
        valid = validate_email(email, check_deliverability=True)
        if valid == EmailNotValidError:
              raise False
        else:
              return True




    def Registro(self, user:S.User_DB, db:Session) -> HTTPException | str:
        if self.Repo.readUs(db, user.email):
            raise HTTPException(status_code =400,detail="Ya existe un usuario como este")

        email_val: bool = self.ValEmail(user.email)

        if not email_val:
            raise HTTPException(status_code= 400,detail="El email es invalido")

        user["password"] = jwt.encode(user.password, SECRET,algorithm=["HS256"])

        self.Repo.createUs(user, db)
        return "Se ha registrado correctamente"


    #[]
    def LogIn(self, user: S.User_DB, db: Session) -> HTTPException | dict:
      
      if not self.Repo.readUs(db, user.email): #Verificamos que exista
            raise HTTPException(status_code =400,detail="El usuario no existe")

      User_DB = self.Repo.readUs(db, user.email) #Ya que existe pedimos su información 

      if not crypt.verify(user.password, User_DB.password): #Comprobamos la contraseña
         raise HTTPException(status_code=400 , detail="Contraseña Incorrecta")

      if not User_DB.email == user.email: #Comprobamos el email
        raise HTTPException(status_code=400 , detail="Nombre Incorrecto")

      Token: dict = {"user":user.email,
                     "exp":datetime.now() + timedelta(minutes=2)}

      return {"access_token": jwt.encode(Token, SECRET, algorithm=["HS256"]), "token_type": "bearer"}  

    def Bearer(self, Token: dict, db: Session) -> S.User:
        try:
          JWT = jwt.decode(Token, SECRET, algorithm=["HS256"]).get("user")
          if JWT == None:
                 raise HTTPException(status_code=401 , detail="Credencial Invalida") #El token no tiene el atributo user
        except JWTError:
                raise HTTPException(status_code=401 , detail="Credencial Invalida")#El Token no puede desencriptarse con las llaves
        
        user = self.Repo.readUs(db, JWT)                        #Traemos el Usuario de Base de Datos, porque existe "user" y pudo desencriptarse
        if not user:                                                 #Si el usuario no existe ERROR
           raise HTTPException(status_code=401,detail="No estas autorizado")
        return user
    
    def InfoUser(self, user: S.User_DB, db: Session) -> pd.DataFrame:
        if not self.Repo.readUs(db, user.email):
            raise HTTPException(status_code =404,detail="El usuario no existe")
        
        self.Repo.readCons(db, user)
        return Consultas
