from sqlalchemy import Table, Integer, Column
from sqlalchemy import ForeignKey
from database import Base

DocumentProjet = Table("document_projet",
    Base.metadata,
    Column('idActeurProjet', Integer, primary_key=True, autoincrement=True),
    Column('idDocument', Integer, ForeignKey('document.idDocument', ondelete='CASCADE', onupdate='CASCADE')),
    Column('idProjet', Integer, ForeignKey('projet.idProjet', ondelete='CASCADE', onupdate='CASCADE'))
)