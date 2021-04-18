from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
from Paciente import Paciente

app = Flask(__name__)
CORS(app)


administrador = {
    "nombreUsuario": "admin",
    "contrasena": "1234"
}

pacientes = []


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
        return jsonify({'agregado': 0, 'mensaje': 'Nombre de usuario ya registrado'})
    contrasena = mensaje['contrasena']
    telefono = mensaje['telefono']
    nuevoPaciente = Paciente(
        nombre, apellido, fechaNacimiento, sexo, nombreUsuario, contrasena, telefono)
    pacientes.append(nuevoPaciente)
    return jsonify({'agregado': 1, 'mensaje': 'Registro exitoso'})


@app.route('/mostrar_pacientes', methods=['GET'])
def mostrarPacientes():
    json_pacientes = []
    global pacientes
    for paciente in pacientes:
        json_pacientes.append(paciente.get_json())
    return jsonify(json_pacientes)


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


if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=puerto)