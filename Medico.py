class Medico():
    def __init__(self,nombre,apellido,fechaNacimiento,sexo,nombreUsuario,contrasena,especialidad,telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.fechaNacimiento = fechaNacimiento
        self.sexo = sexo
        self.nombreUsuario = nombreUsuario
        self.contrasena = contrasena
        self.especialidad = especialidad
        self.telefono = telefono
    
    def get_json(self):
        return {
            "nombre" : self.nombre,
            "apellido" : self.apellido,
            "fechaNacimiento" : self.fechaNacimiento,
            "sexo": self.sexo,
            "nombreUsuario" : self.nombreUsuario,
            "contrasena" : self.contrasena,
            "especialidad" : self.especialidad,
            "telefono" : self.telefono
        }