import app.repositories.TableModels as TM
from sqlalchemy.orm import Session
from app.schemes import Schemas as S
import pandas as pd
#Hashear contraseñas
class Repositorio:
    def __init__(self):
        pass

    def createUs(self, user: S.User_DB, db: Session, UsModel: TM.UserModel = TM.UserModel()) -> None:
        nuevo_producto = TM.Usuario(nombre=user.name, password=user.password, email=user.email)
        db.add(nuevo_producto)
        db.commit()
        db.refresh(TM.Usuario)

    def createCons(self, user: S.User_DB, db:Session, horario, CoModel: TM.ConsultasModel = TM.ConsultasModel()) -> None:
        nuevo_producto = TM.Consulta(horario= horario, usuario= user.name)
        db.add(nuevo_producto)
        db.commit()
        db.refresh(TM.Consulta)

    def readUs(self, db:Session, email: str) -> S.User_DB | None:
           resp = db.get(TM.UserModel, email)
           if not resp:
            return resp
           else:
            Resp = dict(resp)
            return Resp


    def readCons(self, db:Session, user: str,id: int = -1) -> S.Consulta | None:
        resp = db.query(TM.ConsultasModel).where(TM.ConsultasModel.usuario==user)
        if not resp:
               return resp
        resp =  pd.DataFrame(resp)
           #resp.loc[].
        for i in range(len(resp["id"])):
            if id == resp["id"][i]:
               return resp["id"][id] 
        return resp
    
    