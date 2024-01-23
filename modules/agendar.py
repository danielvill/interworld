class Agendar:
    def __init__(self,codigo,nombre,hora,fecha,telefono,direccion,canton,estado):
        self.codigo = codigo
        self.nombre = nombre
        self.hora = hora
        self.fecha = fecha
        self.telefono = telefono
        self.direccion = direccion
        self.canton = canton
        self.estado = estado
        
    def AgeDBCollection(self):
        return{
            "codigo":self.codigo,
            "nombre":self.nombre,
            "hora":self.hora,
            "fecha":self.fecha,
            "telefono":self.telefono,
            "direccion":self.direccion,
            "canton":self.canton,
            "estado":self.estado,
            
        }