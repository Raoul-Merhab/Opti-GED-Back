from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from database import Base

class Workflow(Base):
    __tablename__ = "workflow"
    __table_args__ = {'extend_existing': True}

    idWorkflow : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    projetId : Mapped[int] = mapped_column(ForeignKey('projet.idProjet', ondelete='CASCADE', onupdate='CASCADE'))
    description : Mapped[str] = mapped_column(String(1000))

    def __init__(self, projet : int, description : str):
        self.projet = projet
        self.description = description

    def get_Object(self):
        return {
            "idWorkflow" : self.idWorkflow,
            "projet" : self.projet,
            "description" : self.description
        }