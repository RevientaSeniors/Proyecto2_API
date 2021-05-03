class Compra():
    def __init__(self,nombre,precio,cantidad,subtotal):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.subtotal = subtotal
    
    def get_json(self):
        return {
            "nombre" : self.nombre,
            "precio" : self.precio,
            "cantidad" : self.cantidad,
            "subtotal" : self.subtotal
        }
