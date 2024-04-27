from sqlalchemy import Table, Integer, Column
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from database import Base

Acteur_Projet = Table("acteur_projet",
    Base.metadata,
    Column('idActeurProjet', Integer, primary_key=True, autoincrement=True),
    Column('idActeur', Integer, ForeignKey('acteur.idActeur', ondelete='CASCADE', onupdate='CASCADE')),
    Column('idProjet', Integer, ForeignKey('projet.idProjet', ondelete='CASCADE', onupdate='CASCADE'))
)