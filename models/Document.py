from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from database import Base

class Document(Base):
    __tablename__ = "document"
    __table_args__ = {'extend_existing': True}

    idDocument : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titre : Mapped[str] = mapped_column(String(1000))
    informationsComplementaires : Mapped[str] = mapped_column(String(1000))

    def __init__(self, titre : str, informationsComplementaires : str):
        self.titre = titre
        self.informationsComplementaires = informationsComplementaires

    def get_Object(self):
        return {
            "idDocument" : self.idDocument,
            "titre" : self.titre,
            "informationsComplementaires" : self.informationsComplementaires
        }