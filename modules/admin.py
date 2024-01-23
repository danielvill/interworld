class Admin:
    def __init__(self, user,contraseña,correo):
        self.user = user
        self.contraseña = contraseña
        self.correo = correo

    def AdminDBCollection(self):
        return{
            "user":self.user,
            "contraseña":self.contraseña,
            "correo":self.correo
            
        }