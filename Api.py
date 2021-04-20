from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
from Paciente import Paciente

app = Flask(__name__)
CORS(app)


administrador = {
    "nombre": "Ingrid",
    "apellido": "Perez",
    "nombreUsuario": "admin",
    "contrasena": "1234"
}

pacientes = []
nU = ""



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


@app.route('/mostrar_pacientes', methods=['GET'])
def mostrarPacientes():
    jsonPacientes = []
    global pacientes
    for paciente in pacientes:
        jsonPacientes.append(paciente.get_json())
    return jsonify(jsonPacientes)

@app.route('/datos_paciente', methods=['GET'])
def datosPaciente():
    global pacientes
    global nU
    dPaciente
    for i in pacientes:
        if(nU == i.nombreUsuario):
            dPaciente.append(i.get_json())                       
            return jsonify(dPaciente)
        return jsonify({'estado': 0})

@app.route('/login', methods=['GET'])
def login():
    global pacientes
    nombreUsuario = request.args.get('nombreUsuario')
    contrasena = request.args.get('contrasena')
    if not existeUsuario(nombreUsuario):
        return jsonify({'estado': 0, 'mensaje': 'No existe un usuario con estas credenciales'})
    if nombreUsuario == administrador['nombreUsuario'] and contrasena == administrador['contrasena']:
        return jsonify({'estado': 1, 'mensaje': 'Login exitoso'})
    for paciente in pacientes:
        if nombreUsuario == paciente.nombreUsuario and contrasena == paciente.contrasena:
            return jsonify({'estado': 1, 'mensaje': 'Login exitoso'})
    return jsonify({'estado': 0, 'mensaje': 'Contraseña incorrecta'})  




def existeUsuario(nombreUsuario):
    global pacientes
    if nombreUsuario == administrador['nombreUsuario']:
        return True
    for paciente in pacientes:
        if paciente.nombreUsuario == nombreUsuario:
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

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=puerto)