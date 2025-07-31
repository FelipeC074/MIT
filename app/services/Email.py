from email_validator import validate_emailadress, EmailNotValidError
from smtplib import SMTP_SSL
from email import EmailMessage
from schemes import Schemas as S
import os
from dotenv import load_dotenv
load_dotenv()
passwordE = os.getenv("password")

class Email_Serv(): 
    def __init__(self, email, password):
        email = "CentroMedicodeInvestigaciónyTratamientoyahoomail.com"
        __password = passwordE
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
          valid = validate_emailadress(email, check_deliverability=True)
          if valid == EmailNotValidError:
              raise False
          else:
              return True
        
    def Registro(self, user:S.User) -> str:
        Users: list = "<Soliditud a DB>"
        if user.name in Users:
            raise "Ese nombre ya estâ usado"
        email_val: bool = ValEmail(user.email)
        if not email_val:
            raise "Email no válido"
        """<Solicitud a DB>"""
        return "Se ha registrado correctamente"
    def LogIn(self, user: S.User) :
      Users: 