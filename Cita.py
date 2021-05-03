class Cita():
    def __init__(self,nombreUsuario,fecha,hora,descripcion, estado,medico):
        self.nombreUsuario = nombreUsuario
        self.fecha = fecha
        self.hora = hora
        self.descripcion = descripcion
        self.estado = estado
        self.medico = medico

    def get_json(self):
        return {
            "nombreUsuario" : self.nombreUsuario,
            "fecha" : self.fecha,
            "hora" : self.hora,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "medico": self.medico
        }
