class Estado:
    def __init__(self,codigo,cliente,fecha,direccion,canton):
        self.codigo = codigo
        self.cliente = cliente
        self.fecha = fecha
        self.direccion = direccion
        self.canton = canton
        
        
    def EsDBCollection(self):
        return{
            "codigo":self.codigo,
            "cliente":self.cliente,
            "fecha":self.fecha,
            "direccion":self.direccion,
            "canton":self.canton,
            
        }