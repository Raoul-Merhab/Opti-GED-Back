import jwt

class Token():
    nom : str
    prenom : str
    email : str
    
    def __init__(self, nom, prenom, email):
        self.nom = nom
        self.prenom = prenom
        self.email = email

    def __str__(self):
        return f"{self.nom} {self.prenom} {self.email}"
    # rebi wkilak pyjwt
    def get_token(self):
        return f"{self.nom}${self.prenom}${self.email}"
    
    @staticmethod
    def decode_token(token):
        try:
            temp = token.split("$")
            return Token(temp[0], temp[1], temp[2])
        except:
            return None