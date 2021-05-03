from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
from Paciente import Paciente
from Medicamento import Medicamento
from Medico import Medico
from Enfermera import Enfermera
from Cita import Cita
from Compra import Compra

app = Flask(__name__)
CORS(app)


administrador = {
    "nombre": "Ingrid",
    "apellido": "Perez",
    "nombreUsuario": "admin",
    "contrasena": "1234"
}

pacientes = []
medicamentos =[]
medicos=[]
enfermeras=[]
citas=[]
compras=[]
padecimientos=[]
conteoCitas =[]
uD=""
nM=""
mE=""
meE=""
eE = ""
pE =""

@app.route('/', methods=['GET'])
def principal():
    return jsonify({
        'Nombre :': 'Kenneth Emanuel Solís Ramírez',
        'Carnet :': '201807102'
    })


@app.route('/registro_paciente', methods=['POST'])
def registroPaciente():
    global pacientes
    mensaje = request.get_json()
    nombre = mensaje['nombre']
    apellido = mensaje['apellido']
    fechaNacimiento = mensaje['fechaNacimiento']
    sexo = mensaje['sexo']
    nombreUsuario = mensaje['nombreUsuario']
    if(existeUsuario(nombreUsuario)):
        return jsonify({'estado': 0, 'mensaje': 'Nombre de usuario ya registrado'})
    contrasena = mensaje['contrasena']
    if(contraSegura(contrasena)==False):
        return jsonify({'estado': 0, 'mensaje': 'Contraseña con menos de 8 caracteres'})
    telefono = mensaje['telefono']
    if(camposLLenos(nombre,apellido,fechaNacimiento,sexo,nombreUsuario,contrasena)==False):
        return jsonify({'estado': 0, 'mensaje': 'Hay algún campo vacio'})
    nuevoPaciente = Paciente(nombre, apellido, fechaNacimiento, sexo, nombreUsuario, contrasena, telefono)
    pacientes.append(nuevoPaciente)
    return jsonify({'estado': 1, 'mensaje': 'Registro exitoso'})

@app.route('/editar_paciente', methods=['POST'])
def editarPaciente():
    global pacientes
    global uD
    mensaje = request.get_json()
    if mensaje['nombreAnterior'] == "":
        nombreAnterior = ""
    nombreAnterior = mensaje['nombreAnterior']
    for paciente in pacientes:
        if uD == paciente.nombreUsuario or nombreAnterior == paciente.nombreUsuario:
            paciente.nombre = mensaje['nombre']
            paciente.apellido = mensaje['apellido']
            paciente.fechaNacimiento = mensaje['fechaNacimiento']
            paciente.nombreUsuario = mensaje['nombreUsuario']
            paciente.contrasena = mensaje['contrasena']
            if(contraSegura(paciente.contrasena)==False):
                return jsonify({'estado': 0, 'mensaje': 'Contraseña con menos de 8 caracteres'})
            if(camposLLenos(paciente.nombre,paciente.apellido,paciente.fechaNacimiento,paciente.sexo,paciente.nombreUsuario,paciente.contrasena)==False):
                 return jsonify({'estado': 0, 'mensaje': 'Hay algún campo vacio'})
            uD=paciente.nombreUsuario
            return jsonify({'estado': 1, 'mensaje': 'Actualizacion exitosa'})

            
@app.route('/mostrar_pacientes', methods=['GET'])
def mostrarPacientes():
    json_pacientes = []
    global pacientes
    for paciente in pacientes:
        json_pacientes.append(paciente.get_json())
    return jsonify(json_pacientes)

@app.route('/usuario_dentro', methods=['GET'])
def usuarioDentro():
    global pacientes
    global enfermeras
    global medicos
    global uD
    jsonPaciente = []
    jsonEnfermera =[]
    jsonMedico=[]

    for paciente in pacientes:
        if uD == paciente.nombreUsuario:
            jsonPaciente.append(paciente.get_json())
            return jsonify(jsonPaciente)

    for enfermera in enfermeras:
        if uD == enfermera.nombreUsuario:
            jsonEnfermera.append(enfermera.get_json())
            return jsonify(jsonEnfermera)

    for medico in medicos:
        if uD == medico.nombreUsuario:
            jsonMedico.append(medico.get_json())
            return jsonify(jsonMedico)

    if uD == administrador['nombreUsuario']:
        return jsonify(administrador) 
        
    return jsonify({'aviso': 'error'})      
             

@app.route('/login', methods=['GET'])
def login():
    global pacientes
    global uD
    nombreUsuario = request.args.get('nombreUsuario')
    contrasena = request.args.get('contrasena')
    if not existeUsuario(nombreUsuario):
        return jsonify({'estado': 0, 'mensaje': 'No existe un usuario con estas credenciales'})
    if nombreUsuario == administrador['nombreUsuario'] and contrasena == administrador['contrasena']:
        uD=nombreUsuario
        return jsonify({'estado': 4, 'mensaje': 'Login exitoso'})
    for paciente in pacientes:
        if nombreUsuario == paciente.nombreUsuario and contrasena == paciente.contrasena:
            uD = nombreUsuario
            return jsonify({'estado': 1, 'mensaje': 'Login exitoso'})
    for enfermera in enfermeras:
        if nombreUsuario == enfermera.nombreUsuario and contrasena == enfermera.contrasena:
            uD = nombreUsuario
            return jsonify({'estado': 2, 'mensaje': 'Login exitoso'})
    for medico in medicos:
        if nombreUsuario == medico.nombreUsuario and contrasena == medico.contrasena:
            uD = nombreUsuario
            return jsonify({'estado': 3, 'mensaje': 'Login exitoso'})
            
    return jsonify({'estado': 0, 'mensaje': 'Contraseña incorrecta'})  



def existeUsuario(nombreUsuario):
    global pacientes
    if nombreUsuario == administrador['nombreUsuario']:
        return True
    for paciente in pacientes:
        if paciente.nombreUsuario == nombreUsuario:
            return True
    for enfermera in enfermeras:
        if enfermera.nombreUsuario == nombreUsuario:
            return True
    for medico in medicos:
        if medico.nombreUsuario == nombreUsuario:
            return True
    return False

def contraSegura(contrasena):
    global pacientes
    if len(contrasena) >= 8:
        return True
    return False

def camposLLenos(nombre,apellido,fechaNacimiento,sexo,nombreUsuario,contrasena):
    if(len(nombre) == 0 or len(apellido) == 0 or len(fechaNacimiento) == 0 or len(sexo) == 0 or len(nombreUsuario)==0 or len(contrasena)==0):
        return False
    return True

#Cargas Masivas
@app.route('/carga_medicamentos', methods=['POST'])
def cargaMedicamentos():
    mensaje = request.get_json()
    contenido = mensaje['contenido']
    filas  =  contenido.split("\r\n")
    global medicamentos
    for fila in filas:
        columnas = fila.split(",")
        medicamento = Medicamento(columnas[0],columnas[1],columnas[2],columnas[3])
        medicamentos.append(medicamento)
    return jsonify({"mensaje":"carga masiva exitosa"})

@app.route('/mostrar_medicamentos', methods=['GET'])
def mostrarMedicamentos():
    json_medicamentos = []
    global medicamentos
    for medicamento in medicamentos:
        json_medicamentos.append(medicamento.get_json())
    return jsonify(json_medicamentos)

@app.route('/editar_medicamento', methods=['POST'])
def editarMedicamento():
    global medicamentos
    mensaje = request.get_json()
    nombreAnterior = mensaje['nombreAnterior']
    for medicamento in medicamentos:
        if nombreAnterior == medicamento.nombre:
            medicamento.nombre = mensaje['nombre']
            medicamento.precio = mensaje['precio']
            medicamento.descripcion = mensaje['descripcion']
            medicamento.cantidad = mensaje['cantidad']
            return jsonify({'estado': 1, 'mensaje': 'Actualizacion exitosa'})

@app.route('/eliminar_medicamento', methods=['GET'])
def eliminarMedicamento():
    global medicamentos
    global mE
    medicamentoEliminar = request.args.get('medicamentoEliminar')
    for medicamento in medicamentos:
        if medicamentoEliminar == medicamento.nombre:
            medicamentos.remove(medicamento)
            return jsonify({'mensaje':'Se eliminó correctamente'}) 

@app.route('/carga_medicos', methods=['POST'])
def cargaMedicos():
    global medicos
    mensaje = request.get_json()
    contenido = mensaje['contenido']
    filas  =  contenido.split("\r\n")
    for fila in filas:
        columnas = fila.split(",")
        medico = Medico(columnas[0],columnas[1],columnas[2],columnas[3],columnas[4],columnas[5],columnas[6],columnas[7])
        medicos.append(medico)
    return jsonify({"mensaje":"carga masiva exitosa"})

@app.route('/mostrar_medicos', methods=['GET'])
def mostrarMedicos():
    global medicos
    json_medicos = []
    for medico in medicos:
        json_medicos.append(medico.get_json())
    return jsonify(json_medicos)

@app.route('/editar_medico', methods=['POST'])
def editarMedico():
    global medicos
    mensaje = request.get_json()
    nombreAnterior = mensaje['nombreAnterior']
    for medico in medicos:
        if nombreAnterior == medico.nombreUsuario:
            medico.nombre = mensaje['nombre']
            medico.apellido = mensaje['apellido']
            medico.fechaNacimiento = mensaje['fechaNacimiento']
            medico.nombreUsuario = mensaje['nombreUsuario']
            medico.contrasena = mensaje['contrasena']
            return jsonify({'estado': 1, 'mensaje': 'Actualizacion exitosa'})
    return jsonify({'estado': 0, 'mensaje': 'Actualizacion erronea'})

@app.route('/eliminar_medico', methods=['GET'])
def eliminarMedico():
    global medicos
    global meE
    medicoEliminar = request.args.get('medicoEliminar')
    for medico in medicos:
        if medicoEliminar == medico.nombreUsuario:
            medicos.remove(medico)
            return jsonify({'mensaje':'Se eliminó correctamente'}) 

@app.route('/carga_enfermeras', methods=['POST'])
def cargaEnfermeras():
    global enfermeras
    mensaje = request.get_json()
    contenido = mensaje['contenido']
    filas  =  contenido.split("\r\n")
    for fila in filas:
        columnas = fila.split(",")
        enfermera = Enfermera(columnas[0],columnas[1],columnas[2],columnas[3],columnas[4],columnas[5],columnas[6])
        enfermeras.append(enfermera)
    return jsonify({"mensaje":"carga masiva exitosa"})

@app.route('/mostrar_enfermeras', methods=['GET'])
def mostrarEnfermeras():
    global enfermeras 
    json_enfermeras = []
    for enfermera in enfermeras:
        json_enfermeras.append(enfermera.get_json())
    return jsonify(json_enfermeras)

@app.route('/editar_enfermera', methods=['POST'])
def editarEnfermera():
    global enfermeras
    mensaje = request.get_json()
    nombreAnterior = mensaje['nombreAnterior']
    for enfermera in enfermeras:
        if nombreAnterior == enfermera.nombreUsuario:
            enfermera.nombre = mensaje['nombre']
            enfermera.apellido = mensaje['apellido']
            enfermera.fechaNacimiento = mensaje['fechaNacimiento']
            enfermera.nombreUsuario = mensaje['nombreUsuario']
            enfermera.contrasena = mensaje['contrasena']
            return jsonify({'estado': 1, 'mensaje': 'Actualizacion exitosa'})
    return jsonify({'estado': 0, 'mensaje': 'Actualizacion erronea'})

@app.route('/eliminar_enfermera', methods=['GET'])
def eliminarEnfermera():
    global enfermeras
    global eE
    enfermeraEliminar = request.args.get('enfermeraEliminar')
    for enfermera in enfermeras :
        if enfermeraEliminar == enfermera.nombreUsuario:
            enfermeras.remove(enfermera)
            return jsonify({'mensaje':'Se eliminó correctamente'})

@app.route('/carga_pacientes', methods=['POST'])
def cargaPacientes():
    global pacientes
    mensaje = request.get_json()
    contenido = mensaje['contenido']
    filas  =  contenido.split("\r\n")
    for fila in filas:
        columnas = fila.split(",")
        paciente = Paciente(columnas[0],columnas[1],columnas[2],columnas[3],columnas[4],columnas[5],columnas[6])
        pacientes.append(paciente)
    return jsonify({"mensaje":"carga masiva exitosa"})


@app.route('/eliminar_paciente', methods=['GET'])
def eliminarPaciente():
    global pacientes
    global pE
    pacienteEliminar = request.args.get('pacienteEliminar')
    for paciente in pacientes :
        if pacienteEliminar == paciente.nombreUsuario:
            pacientes.remove(paciente)
            return jsonify({'mensaje':'Se eliminó correctamente'})


@app.route('/registro_cita', methods=['POST'])
def registroCita():
    global citas
    global uD
    mensaje = request.get_json()
    nombreUsuario = uD
    for cita in citas:
        if nombreUsuario == cita.nombreUsuario:
            if cita.estado =="Aceptada" or cita.estado =="Pendiente":
                return jsonify({'estado': 0, 'mensaje': 'Ya tiene una cita a su nombre'})
    fecha = mensaje['fecha']
    hora = mensaje['hora']
    descripcion = mensaje['descripcion']
    nuevaCita = Cita(nombreUsuario, fecha, hora, descripcion,"Pendiente","")
    citas.append(nuevaCita)
    return jsonify({'estado': 1, 'mensaje': 'Registro exitoso de la cita'})

@app.route('/mostrar_citas', methods=['GET'])
def mostrarCitas():
    global citas
    json_citas = []
    for cita in citas:
        json_citas.append(cita.get_json())
    return jsonify(json_citas)

@app.route('/editar_cita', methods=['POST'])
def editarCita():
    global citas
    global uD
    mensaje = request.get_json()
    nombreUsuarioP = mensaje['nombreUsuarioP']
    if mensaje['medico'] == "":
        mensaje['medico'] = uD
    for cita in citas:
        if nombreUsuarioP == cita.nombreUsuario:
            cita.estado = mensaje['estado']
            cita.medico = mensaje['medico']
            return jsonify({'estado': 1, 'mensaje': 'Cambio exitoso'})

@app.route('/mostrar_cita', methods=['GET'])
def mostrarCita():
    global citas
    global uD
    json_cita = []
    for cita in citas:
        if uD == cita.nombreUsuario:
            json_cita.append(cita.get_json())
            return jsonify(json_cita)

@app.route('/registro_compra', methods=['POST'])
def registroCompra():
    global compras
    mensaje = request.get_json()
    nombre = mensaje['nombre']
    for compra in compras:
        if nombre == compra.nombre:
            num1 = int(compra.cantidad)
            num2 = int(mensaje['cantidad'])
            cantidad = num1+num2
            compra.cantidad = cantidad
            return jsonify({'estado': 1, 'mensaje': 'Registro exitoso de la compra'})
    precio = mensaje['precio']
    cantidad = mensaje['cantidad']
    subtotal = mensaje['subtotal']
    nuevaCompra = Compra(nombre, precio, cantidad, subtotal)
    compras.append(nuevaCompra)
    return jsonify({'estado': 1, 'mensaje': 'Registro exitoso de la compra'})

@app.route('/mostrar_compras', methods=['GET'])
def mostrarCompras():
    global compras
    json_compras = []
    for compra in compras:
        json_compras.append(compra.get_json())
    return jsonify(json_compras)

@app.route('/registro_padecimiento', methods=['POST'])
def registroPadecimiento():
    global padecimientos
    mensaje = request.get_json()
    nombrePadecimiento = mensaje['nombrePadecimiento']
    padecimientos.append(mensaje)
    return jsonify({'estado': 1, 'mensaje': 'Registro exitoso del Padecimiento'})

@app.route('/mostrar_padecimientos', methods=['GET'])
def mostrarPadecimientos():
    global padecimientos
    json_padecimientos = []
    return jsonify(padecimientos)

@app.route('/registro_conteo', methods=['POST'])
def registroConteo():
    global conteoCitas
    mensaje = request.get_json()
    conteoCitas.append(mensaje)
    return jsonify({'estado': 1, 'mensaje': 'Registro exitoso del contador'})

@app.route('/mostrar_conteo', methods=['GET'])
def mostrarConteo():
    global conteoCitas
    return jsonify(conteoCitas)

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=puerto)