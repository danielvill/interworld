class Agendar:
    def __init__(self,tecnico,cliente,hora,fecha,telefono,direccion,canton,estado):
        self.tecnico = tecnico
        self.cliente = cliente
        self.hora = hora
        self.fecha = fecha
        self.telefono = telefono
        self.direccion = direccion
        self.canton = canton
        self.estado = estado
        
    def AgeDBCollection(self):
        return{
            "tecnico":self.tecnico,
            "cliente":self.cliente,
            "hora":self.hora,
            "fecha":self.fecha,
            "telefono":self.telefono,
            "direccion":self.direccion,
            "canton":self.canton,
            "estado":self.estado,
            
        }