import TableModels as TM
from sqlalchemy.orm import Session
from schemes import Schemas as S

class Repositorio:
    def __init__(self):
        pass

    def createUs(self, user: S.User, db: Session, UsModel: TM.UserModel = TM.UserModel()) -> None:
        nuevo_producto = Usuario(nombre=user.name, password=user.password, email=user.email)
        db.add(nuevo_producto)
        db.commit()
        db.refresh(Usuario)

    def createCons(self, user: S.User, db:Session, CoModel: TM.ConsultasModel = TM.ConsultasModel(), horario) -> None:
        nuevo_producto = Consulta(horario= horario, usuario= user.name)
        db.add(nuevo_producto)
        db.commit()
        db.refresh(Consulta)

    def readUs(self, user: S.User | bool = False, db:Session) -> S.User:
        if user != False:
           resp = db.query(TM.UserModel).where(name==user.name)
        else: 
            resp = db.query(TM.UserModel).all()
        #Transformacion de type(resp) a S.User
        return Usuario
    def readCons(self, user: S.User | bool = False, db:Session) -> S.User:
        if user != False:
           resp = db.query(TM.UserModel).where(name==user.name)
        else: 
            resp = db.query(TM.UserModel).all()
        #Transformacion de type(resp) a S.User
        return Usuario
        