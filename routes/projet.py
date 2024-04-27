from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from models.Projet import Projet
from models.Acteur import Acteur
from models.User import User
from models.Workflow import Workflow
from models.Document import Document
from sqlalchemy import update
from pydantic import BaseModel
from utils.Token import Token
from controllers.IntelligentStuff import IntelligentStuff

class Projets(BaseModel):
    token : str

class ProjetToAdd(BaseModel):
    token : str
    nom : str
    description : str

class ProjetToEdit(BaseModel):
    token : str
    idProjet : int
    nom : str = None
    description : str = None
    class Acteur(BaseModel):
        action : str
        idActeur : int = None
        nom : str = None
        role : str = None
        departement : str = None
    acteur : Acteur = None
    class Document(BaseModel):
        action : str
        idDocument : int = None
        titre : str = None
        info : str = None
    document : Document = None
    class Workflow(BaseModel):
        action : str
        idWorkflow : int = None
        description : str = None    
    workflow : Workflow = None
    pdf_base64 : str = None

class ProjetToSearch(BaseModel):
    token : str
    keywords : str

class ProjetToSuggerer(BaseModel):
    token : str
    base64 : str
router = APIRouter()

@router.post("/projets")
def get_projet(projet: Projets, db: Session = Depends(get_db)):
    print(projet)
    check = Token.decode_token(projet.token)
    if ( not check ):
        return {
            "Status": "Error",
            "Message": "Invalid token"
        }
    user = db.query(User).filter(User.email == check.email).first()
    return {
        "Status": "Success",
        "Data": db.query(Projet).where(Projet.user_id == user.idUser).all()
    }

@router.get("/{idProjet}")
def get_projet_by_id(idProjet: int, db: Session = Depends(get_db)):
    # check = Token.decode_token(token)
    # if ( not check ):
    #     return {
    #         "Status": "Error",
    #         "Message": "Invalid token"
    #     }
    return db.query(Projet).filter(Projet.idProjet == idProjet).first()

@router.post("/search-projet")
def search_projet(search: ProjetToSearch, db: Session = Depends(get_db)):
    check = Token.decode_token(search.token)
    if ( not check ):
        return {
            "Status": "Error",
            "Message": "Invalid token"
        }
    projets = db.query(Projet).all()
    result = []
    for projet in projets:
        if ( search.keywords in projet.nom or search.keywords in projet.description ):
            result.append(projet)
    return{
        "Status": "Success",
        "Data": result
    }

@router.post("/ajouter-projet")
def ajouter_projet(projet: ProjetToAdd, db: Session = Depends(get_db)):
    check = Token.decode_token(projet.token)
    if ( not check ):
        return {
            "Status": "Error",
            "Message": "Invalid token"
        }
    print(projet.nom)
    print(projet.description)
    if ( not projet.nom or not projet.description):
        return {
            "Status": "Error",
            "Message": "Missing information"
        }
    user = db.query(User).filter(User.email == check.email).first()
    if ( not user ):
        return {
            "Status": "Error",
            "Message": "User not found"
        }
    Lprojet = Projet(nom=projet.nom, description=projet.description,user_id=user.idUser )
    db.add(Lprojet)
    db.commit()
    db.refresh(Lprojet)
    return {
        "Status": "Success",
        "Data": Lprojet
    }

@router.post("/modifier-projet")
def modifier_projet(projet: ProjetToEdit, db: Session = Depends(get_db)):
    check = Token.decode_token(projet.token)
    if ( not check ):
        return {
            "Status": "Error",
            "Message": "Invalid token"
        }
    if ( ProjetToEdit.idProjet is None):
        return {
            "Status": "Error",
            "Message": "Missing project id"
        }
    if ( projet.nom ):
        projet = db.query(Projet).filter(Projet.idProjet == ProjetToEdit.idProjet).first()
        update(projet).values(nom=ProjetToEdit.nom)
        db.commit()
        return {
            "Status": "Success",
            "Message": "Projet updated"
        }
    elif ( projet.description ):
        projet = db.query(Projet).filter(Projet.idProjet == ProjetToEdit.idProjet).first()
        update(projet).values(description=ProjetToEdit.description)
        db.commit()
        return {
            "Status": "Success",
            "Message": "Projet updated"
        }
    elif ( projet.acteur ):
        if ( projet.acteur.action == "ajouter" and projet.acteur.nom and projet.acteur.role and projet.acteur.departement ):
            acteur = Acteur(nom=projet.acteur.nom, role=projet.acteur.role, departement=projet.acteur.departement)
            db.add(acteur)
            db.commit()
            db.refresh(acteur)
            return acteur
        elif ( projet.acteur.action == "modifier" and projet.acteur.idActeur and (projet.acteur.nom or projet.acteur.role or projet.acteur.departement) ):
            acteur = db.query(Acteur).filter(Acteur.idActeur == ProjetToEdit.acteur.idActeur).first()
            if ( projet.acteur.nom ):
                update(acteur).values(nom=projet.acteur.nom)
                db.commit()
            elif ( projet.acteur.role ):
                update(acteur).values(role=projet.acteur.role)
                db.commit()
            elif ( projet.acteur.departement ):
                update(acteur).values(departement=projet.acteur.departement)
                db.commit()
            return {
                "Status": "Success",
                "Message": "Acteur updated"
            }
        elif ( projet.acteur.action == "supprimer" and projet.acteur.idActeur ):
            projet = db.query(Projet).filter(Projet.idProjet == ProjetToEdit.idProjet).first()
            acteur = db.query(Acteur).filter(Acteur.idActeur == projet.acteur.idActeur).first()
            projet.acteurs.remove(acteur)
            db.delete(acteur)
            db.commit()
            return {
                "Status": "Success",
                "Message": "Acteur deleted"
            }
        else:
            return {
                "Status": "Error",
                "Message": "Missing information"
            }
    elif ( projet.workflow ):
        if ( projet.workflow.action == "ajouter" and projet.workflow.description ):
            labase64 = projet.workflow.description
            text = IntelligentStuff.diagram_to_text(labase64)
            workflow = Workflow(description=text, projet=projet.idProjet)
            Lprojet = db.query(Projet).where(Projet.idProjet == projet.idProjet).first()
            Lprojet.workflows.append(workflow)
            db.commit()
            return workflow
        elif ( projet.workflow.action == "modifier" and projet.workflow.idWorkflow and projet.workflow.description ):
            labase64 = projet.workflow.description
            text = IntelligentStuff.diagram_to_text(labase64)
            workflow = db.query(Workflow).filter(Workflow.idWorkflow == projet.workflow.idWorkflow).first()
            update(workflow).values(description=text)
            db.commit()
            return {
                "Status": "Success",
                "Message": "Workflow updated"
            }
        elif ( projet.workflow.action == "supprimer" and projet.workflow.idWorkflow ):
            workflow = db.query(Workflow).filter(Workflow.idWorkflow == projet.workflow.idWorkflow).first()
            db.delete(workflow)
            db.commit()
            return {
                "Status": "Success",
                "Message": "Workflow deleted"
            }
        else:
            return {
                "Status": "Error",
                "Message": "Missing information"
            }
    elif ( projet.document ):
        if ( projet.document.action == "ajouter" and projet.document.titre and projet.document.info ):
            document = Document(titre=projet.document.titre, info=projet.document.info, projet=projet.idProjet)
            Lprojet = db.query(Projet).where(Projet.idProjet == projet.idProjet).first()
            Lprojet.documents.append(document)
            db.commit()
            return document
        elif ( projet.document.action == "modifier" and projet.document.idDocument and (projet.document.titre or projet.document.info) ):
            document = db.query(Document).filter(Document.idDocument == projet.document.idDocument).first()
            if ( projet.document.titre ):
                update(document).values(titre=projet.document.titre)
                db.commit()
            elif ( projet.document.info ):
                update(document).values(info=projet.document.info)
                db.commit()
            return {
                "Status": "Success",
                "Message": "Document updated"
            }
        elif ( projet.document.action == "supprimer" and projet.document.idDocument ):
            Lprojet = db.query(Projet).where(Projet.idProjet == projet.idProjet).first()
            document = db.query(Document).filter(Document.idDocument == projet.document.idDocument).first()
            Lprojet.documents.remove(document)
            db.delete(document)
            db.commit()
            return {
                "Status": "Success",
                "Message": "Document deleted"
            }
        else:
            return {
                "Status": "Error",
                "Message": "Missing information"
            }
    elif ( projet.pdf_base64 ):
        labase64 = projet.pdf_base64
        workflows = IntelligentStuff.pdf_to_jpegs(labase64)
        for workflow in workflows:
            LWorkflow = Workflow(description=text, projet=projet.idProjet)
            Lprojet = db.query(Projet).where(Projet.idProjet == projet.idProjet).first()
            Lprojet.workflows.append(LWorkflow)
            db.commit()
        return {
            "Status": "Success",
            "Message": "Workflows added"
        }
    else:
        return {
            "Status": "Error",
            "Message": "Missing information"
        }

@router.post("/supprimer-projet")
def supprimer_projet(token: str, idProjet: int, db: Session = Depends(get_db)):
    check = Token.decode_token(token)
    if ( not check ):
        return {
            "Status": "Error",
            "Message": "Invalid token"
        }
    projet = db.query(Projet).filter(Projet.idProjet == idProjet).first()
    db.delete(projet)
    db.commit()
    return {
        "Status": "Success",
        "Message": "Projet deleted"
    }

@router.post("/suggerer-workflow")
def suggerer_workflow(projet: ProjetToSuggerer, db: Session = Depends(get_db)):
    check = Token.decode_token(projet.token)
    if ( not check ):
        return {
            "Status": "Error",
            "Message": "Invalid token"
        }
    return {
        "Status": "Success",
        "Data": IntelligentStuff.suggerer_workflow(projet.base64)
    }    
