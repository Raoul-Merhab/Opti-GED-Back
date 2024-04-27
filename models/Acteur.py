from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from database import Base

class Acteur(Base):
    __tablename__ = "acteur"
    __table_args__ = {'extend_existing': True}

    idActeur : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nom : Mapped[str] = mapped_column(String(1000))
    role : Mapped[str] = mapped_column(String(1000))
    departement : Mapped[str] = mapped_column(String(1000))

    def __init__(self, nom : str, role : str, departement):
        self.nom = nom
        self.role = role
        self.departement = departement

    def get_Object(self):
        return {
            "idActeur" : self.idActeur,
            "nom" : self.nom,
            "role" : self.role,
            "departement" : self.departement
        }