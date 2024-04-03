class Estado:
    def __init__(self,tecnico,cliente,fecha,direccion,canton):
        self.tecnico = tecnico
        self.cliente = cliente
        self.fecha = fecha
        self.direccion = direccion
        self.canton = canton
        
        
    def EsDBCollection(self):
        return{
            "tecnico":self.tecnico,
            "cliente":self.cliente,
            "fecha":self.fecha,
            "direccion":self.direccion,
            "canton":self.canton,
            
        }