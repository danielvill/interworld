class Tecnico:
    def __init__(self, user,contraseña,correo):
        self.user = user
        self.contraseña = contraseña
        self.correo = correo

    def TecniDBCollection(self):
        return{
            "user":self.user,
            "contraseña":self.contraseña,
            "correo":self.correo 
        }