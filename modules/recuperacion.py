class Recuperacion:
    def __init__(self, user,correo):
        self.user = user
        self.correo = correo
        
    def RecuDBCollection(self):
        return{
            "user":self.user,
            "correo":self.correo,
        }