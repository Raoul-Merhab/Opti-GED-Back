from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from database import Base

from models.Acteur import Acteur
from models.Document import Document
from models.Workflow import Workflow

from models.ActeurProjet import Acteur_Projet
from models.DocumentProjet import DocumentProjet

class Projet(Base):
    __tablename__ = "projet"
    __table_args__ = {'extend_existing': True}

    idProjet : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nom : Mapped[str] = mapped_column(String(1000))
    description : Mapped[str] = mapped_column(String(1000))
    user_id : Mapped[int] = mapped_column(ForeignKey('user.idUser', ondelete='CASCADE', onupdate='CASCADE'))

    acteurs : Mapped[list["Acteur"]] = relationship(secondary=Acteur_Projet)
    documents : Mapped[list["Document"]] = relationship(secondary=DocumentProjet)
    # workflows : Mapped[list["Workflow"]] = relationship(back_populates="projet")

    def __init__(self, nom : str, description : str, user_id : int):
        self.user_id = user_id
        self.nom = nom
        self.description = description
        self.acteurs = []
        self.documents = []
        self.workflows = []

    def get_Object(self):
        return {
            "idProjet" : self.idProjet,
            "nom" : self.nom,
            "user_id":self.user_id,
            "description" : self.description,
            "acteurs" : [*map(lambda x: x.get_Object(), self.acteurs)],
            "documents" : [*map(lambda x: x.get_Object(), self.documents)],
            "workflows" : [*map(lambda x: x.get_Object(), self.workflows)],
        }