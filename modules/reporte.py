class Reporte:
    def __init__(self,codigo,cliente,fecha,direccion,canton,comentario,estado):
        self.codigo = codigo
        self.cliente = cliente
        self.fecha = fecha
        self.direccion = direccion
        self.canton = canton
        self.comentario = comentario
        self.estado = estado
        
    def RepoDBCollection(self):
        return{
            "codigo":self.codigo,
            "cliente":self.cliente,
            "fecha":self.fecha,
            "direccion":self.direccion,
            "canton":self.canton,
            "comentario":self.comentario,
            "estado":self.estado
        }