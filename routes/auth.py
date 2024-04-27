from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from models.User import User
from pydantic import BaseModel
from utils.Token import Token

from passlib.hash import sha256_crypt


class UserToSignUp(BaseModel):
    nom : str
    prenom : str
    email : str
    password : str

router = APIRouter()

# Works
@router.post("/signup")
def signup(user : UserToSignUp, db : Session = Depends(get_db)):
    serach = db.query(User).filter(User.email == user.email).first()
    if ( serach ):
        return {
            "Status": "Error",
            "Message": "Email already exists"
        }
    newUser = User(nom=user.nom, prenom=user.prenom, email=user.email, password=sha256_crypt.hash(user.password))
    token = Token(nom=user.nom, prenom=user.prenom, email=user.email)
    db.add(newUser)
    db.commit()
    return {
        "Status": "Success",
        "Token": token.get_token()
    }

class UserToSignIn(BaseModel):
    email : str
    password : str

@router.post("/signin")
def signin(user : UserToSignIn, db : Session = Depends(get_db)):
    search = db.query(User).filter(User.email == user.email).first()
    if ( search and sha256_crypt.verify(user.password, search.password)):
        token = Token(nom=search.nom, prenom=search.prenom, email=search.email)
        return {
            "Status": "Success",
            "Token": token.get_token()
        }
    return {
        "Status": "Error",
        "Message": "Email or password incorrect"
    }
