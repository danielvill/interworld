class Reporte:
    def __init__(self,tecnico,cliente,fecha,direccion,canton,comentario,estado):
        self.tecnico = tecnico
        self.cliente = cliente
        self.fecha = fecha
        self.direccion = direccion
        self.canton = canton
        self.comentario = comentario
        self.estado = estado
        
    def RepoDBCollection(self):
        return{
            "tecnico":self.tecnico,
            "cliente":self.cliente,
            "fecha":self.fecha,
            "direccion":self.direccion,
            "canton":self.canton,
            "comentario":self.comentario,
            "estado":self.estado
        }