import app.repositories.TableModels as TM
from sqlalchemy.orm import Session
from app.schemes import Schemas as S
import pandas as pd
#Hashear contraseñas
class Repositorio:
    def __init__(self):
        pass

    def createUs(self, user: S.User, db: Session, UsModel: TM.UserModel = TM.UserModel()) -> None:
        nuevo_user = TM.Usuario(nombre=user.name, password=user.password, email=user.email)
        db.add(nuevo_user)
        db.commit()
        db.refresh(nuevo_user)

    def createCons(self, user: S.User, db:Session, horario, CoModel: TM.ConsultasModel = TM.ConsultasModel()) -> None:
        nueva_cons = TM.Consulta(horario= horario, usuario= user.name)
        db.add(nueva_cons)
        db.commit()
        db.refresh(nueva_cons)

    def readUs(self, db:Session, email: str) -> S.User_DB | None:
           # db.get() returns a UserModel instance or None
           user_db = db.get(TM.UserModel, email)
           if user_db:
            # Convert the SQLAlchemy model to a Pydantic model
            return S.User_DB.model_validate(user_db)
           return None

    def readCons(self, db:Session, user: str, id: int = -1) -> list[S.Consulta] | S.Consulta | None:
        # 1. Create the base query
        query = db.query(TM.ConsultasModel).filter(TM.ConsultasModel.usuario == user)

        # 2. If ID is specified, filter by it and get the first result
        if id != -1:
            # .first() executes the query and returns one model instance or None
            consulta_db = query.filter(TM.ConsultasModel.id == id).first()
            if consulta_db:
                # Convert the single instance to a Pydantic model
                return S.Consulta.model_validate(consulta_db)
            return None
        
        # 3. If no ID, get all results
        # .all() executes the query and returns a list of model instances
        consultas_db = query.all()
        if not consultas_db:
            return None
        
        # Convert the list of instances to a list of Pydantic models
        return [S.Consulta.model_validate(c) for c in consultas_db]