
import datetime
import os

os.environ['SERVER_HOST'] = 'localhost'  # Establecer el host
os.environ['SERVER_PORT'] = '8086'  # Establecer el puerto

from flask import Flask, render_template, request, jsonify
from BBDD import gestionBBDD
from Utiles import Validadores
from datetime import datetime

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def home():
    return  render_template("index.html")


@app.get('/Cliente')
def GetUser():
    """Retrieve customer information."""
    dni = request.args.get("DNI")
    if not dni:
        return jsonify({"error": "El parametro 'DNI' es obligatorio"}), 400
    if not Validadores.ValidarDNI(dni):
        return jsonify({"error": "El DNI introducido no es valido"}), 400

    # Consulta parametrizada para evitar inyecciones SQL
    query = "SELECT * FROM tbClientes WHERE DNI = ?"
    client = gestionBBDD.query_db(query, [dni], one=True)

    if client is None:
        return jsonify({"error": "Cliente no encontrado"}), 404

    # Convierte la fila en un diccionario para devolver como JSON
    return jsonify(dict(client))

@app.post('/Cliente')
def CreateUser():
    # Obtener los datos enviados en formato JSON
    data = request.get_json()

    # Validar los campos requeridos
    required_fields = ["DNI", "Nombre", "Email", "CapitalSolicitado"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"El campo '{field}' es obligatorio"}), 400

    # Extraer datos
    dni = data["DNI"]
    nombre = data["Nombre"]
    email = data["Email"]
    capital = data["CapitalSolicitado"]
    
    if not Validadores.ValidarDNI(dni):
        return jsonify({"error": "El DNI introducido no es valido"}), 400

    # Insertar en la base de datos
    query = """
        INSERT INTO tbClientes (DNI, Nombre, Email, CapitalSolicitado)
        VALUES (?, ?, ?, ?)
    """
    try:
        gestionBBDD.query_db(query, [dni, nombre, email, capital])
        gestionBBDD.get_db().commit()  # Confirmar los cambios
        return jsonify({"message": "Cliente agregado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al agregar cliente: {str(e)}"}), 500

@app.put('/Cliente')
def UpdateUser():
    # Obtener los datos enviados en formato JSON
    data = request.get_json()

    # Validar los campos requeridos
    if "DNI" not in data:
        return jsonify({"error": "El campo 'DNI' es obligatorio"}), 400

    # Extraer datos
    dni = data["DNI"]
    nombre = data.get("Nombre")  # Puede ser opcional
    email = data.get("Email")    # Puede ser opcional
    capital = data.get("CapitalSolicitado")  # Puede ser opcional
    
    if not Validadores.ValidarDNI(dni):
        return jsonify({"error": "El DNI introducido no es valido"}), 400

    # Construir consulta dinámicamente en función de los campos enviados
    updates = []
    params = []

    if nombre:
        updates.append("Nombre = ?")
        params.append(nombre)
    if email:
        updates.append("Email = ?")
        params.append(email)
    if capital:
        updates.append("CapitalSolicitado = ?")
        params.append(capital)

    if not updates:
        return jsonify({"error": "No se proporcionaron campos para actualizar"}), 400

    # Agregar el DNI al final de los parámetros para la cláusula WHERE
    params.append(dni)

    query = f"UPDATE tbClientes SET {', '.join(updates)} WHERE DNI = ?"

    try:
        rows_affected = gestionBBDD.query_db(query, params)
        gestionBBDD.get_db().commit()  # Confirmar los cambios

        if rows_affected == 0:
            return jsonify({"error": "Cliente no encontrado"}), 404

        return jsonify({"message": "Cliente actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar cliente: {str(e)}"}), 500


@app.delete('/Cliente')
def DeleteUser():
    # Obtener los datos enviados en formato JSON
    data = request.get_json()

    # Validar el campo obligatorio
    if "DNI" not in data:
        return jsonify({"error": "El campo 'DNI' es obligatorio"}), 400

    dni = data["DNI"]

    
    if not Validadores.ValidarDNI(dni):
        return jsonify({"error": "El DNI introducido no es valido"}), 400

    # Eliminar el cliente
    query = "DELETE FROM tbClientes WHERE DNI = ?"

    try:
        rows_affected = gestionBBDD.query_db(query, [dni])
        gestionBBDD.get_db().commit()  # Confirmar los cambios

        if rows_affected == 0:
            return jsonify({"error": "Cliente no encontrado"}), 404

        return jsonify({"message": "Cliente eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar cliente: {str(e)}"}), 500


@app.get('/Simulacion')
def GetSimulacionUsuario():
    """Retrieve customer information."""
    dni = request.args.get("DNI")
    tae = request.args.get("TAE")
    plazo = request.args.get("PLAZO")

    if not dni:
        return jsonify({"error": "El parametro 'DNI' es obligatorio"}), 400
    if not tae:
        return jsonify({"error": "El parametro 'TAE' es obligatorio"}), 400
    if not plazo:
        return jsonify({"error": "El parametro 'PLAZO' es obligatorio"}), 400
    if not Validadores.ValidarDNI(dni):
        return jsonify({"error": "El DNI introducido no es valido"}), 400

    try:
        tae = float(tae)  # Intenta convertir a float
    except ValueError:
        return jsonify({"error": "El TAE introducido no es valido"}), 400

    try:
        plazo = float(plazo)  # Intenta convertir a float
    except ValueError:
        return jsonify({"error": "El PLAZO introducido no es valido"}), 400

    # Consulta parametrizada para evitar inyecciones SQL
    query = "SELECT * FROM tbClientes WHERE DNI = ?"
    client = gestionBBDD.query_db(query, [dni], one=True)

    if client is None:
        return jsonify({"error": "Cliente no encontrado"}), 404

    capital = dict(client)["CapitalSolicitado"]
    i = (float(tae)/100)/12
    n = float(plazo)*12
    cuota = (capital * i) / (1 - (1 + i) ** (-n))
    importeTotal = cuota * n

        # Insertar en la base de datos
    query = """
        INSERT INTO tbSimulaciones (DNI, Capital, Tae, Plazo, CuotaMensual, ImporteTotal, FechaSimulacion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    try:
        gestionBBDD.query_db(query, [dni, capital, tae, plazo, cuota, importeTotal, datetime.now()])
        gestionBBDD.get_db().commit()  # Confirmar los cambios
    except Exception as e:
        return jsonify({"error": f"Error al guardar informacion de simulacion: {str(e)}"}), 500

    # Convierte la fila en un diccionario para devolver como JSON
    return jsonify({"message": f"Cuota mensual: {str(cuota)}, Total a devolver {str(importeTotal)}"}), 200


if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '8086'))
    except ValueError:
        PORT = 8086
    app.run(host=HOST, port=PORT)
