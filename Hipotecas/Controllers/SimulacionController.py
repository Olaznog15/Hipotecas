
from flask import Flask, make_response, request, jsonify
from BBDD import gestionBBDD
from Utiles import Validadores
from datetime import datetime
from flask_restx import Api, Namespace, Resource, fields, reqparse

SimulacionCtrl = Namespace("Simulacion", path="/Simulacion", description ="Simulacion API Controller")

parser = reqparse.RequestParser()
parser.add_argument("DNI", type=str)
parser.add_argument("TAE", type=str)
parser.add_argument("PLAZO", type=str)

@SimulacionCtrl.route("")
class Simulacion(Resource):
    @SimulacionCtrl.expect(parser)
    def get(self):
        dni = request.args.get("DNI").upper()
        tae = request.args.get("TAE")
        plazo = request.args.get("PLAZO")

        if not dni:            
            resp = make_response(jsonify({"error": "El parametro 'DNI' es obligatorio"}), 400)
            return resp
        if not tae:            
            resp = make_response(jsonify({"error": "El parametro 'TAE' es obligatorio"}), 400)
            return resp
        if not plazo:            
            resp = make_response(jsonify({"error": "El parametro 'PLAZO' es obligatorio"}), 400)
            return resp
        if not Validadores.ValidarDNI(dni):            
            resp = make_response(jsonify({"error": "El DNI introducido no es valido"}), 400)
            return resp

        try:
            tae = float(tae)  # Intenta convertir a float
        except ValueError:   
            resp = make_response(jsonify({"error": "El TAE introducido no es valido"}), 400)
            return resp

        try:
            plazo = float(plazo)  # Intenta convertir a float
        except ValueError:
            resp = make_response(jsonify({"error": "El PLAZO introducido no es valido"}), 400)
            return resp

        # Consulta parametrizada para evitar inyecciones SQL
        query = "SELECT * FROM tbClientes WHERE DNI = ?"
        client = gestionBBDD.query_db(query, [dni], one=True)

        if client is None:
            return jsonify({"error": "Cliente no encontrado"})

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
            resp = make_response(jsonify({"error": f"Error al guardar informacion de simulacion: {str(e)}"}), 500)
            return resp

        # Convierte la fila en un diccionario para devolver como JSON
        dictionary = {
            "Mensual": cuota,
            "Total": importeTotal
        }
        return jsonify(dictionary)