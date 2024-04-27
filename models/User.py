from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from database import Base

class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    idUser : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nom : Mapped[str] = mapped_column(String(1000))
    prenom : Mapped[str] = mapped_column(String(1000))
    email : Mapped[str] = mapped_column(String(1000))
    password : Mapped[str] = mapped_column(String(1000))

    def __init__(self, nom : str, prenom : str, email : str, password : str):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.password = password
        
    def get_Object(self):
        return {
            "idUser" : self.idUser,
            "nom" : self.nom,
            "prenom" : self.prenom,
            "email" : self.email
        }