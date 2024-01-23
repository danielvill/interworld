class Recuperacion:
    def __init__(self, user,contraseña):
        self.user = user
        self.contraseña = contraseña
        
    def RecuDBCollection(self):
        return{
            "user":self.user,
            "contraseña":self.contraseña,
        }