class Medicamento():
    def __init__(self,nombre,precio,descripcion,cantidad):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.cantidad = cantidad
    
    def get_json(self):
        return {
            "nombre" : self.nombre,
            "precio" : self.precio,
            "descripcion" : self.descripcion,
            "cantidad" : self.cantidad
        }
