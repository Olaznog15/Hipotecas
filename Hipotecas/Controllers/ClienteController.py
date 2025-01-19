
from flask import Flask, make_response, request, jsonify
from BBDD import gestionBBDD
from Utiles import Validadores
from flask_restx import Api, Namespace, Resource, fields, reqparse

ClienteCtrl = Namespace("Cliente", path="/Cliente", description ="Clientes API Controller")
CrearclienteCommand = ClienteCtrl.model("CrearclienteCommand",{
    'DNI': fields.String(required=True, description='dni', example ="00000000T"),
    'Nombre': fields.String(required=True, description='Namespacenombre', example ="Gonzalo Montero"),
    'Email': fields.String(required=True, description='email', example ="gonzalo.montero15@gmail.com"),
    'CapitalSolicitado': fields.String(required=True, description='capital', example ="250000")
    })
EliminarclienteCommand= ClienteCtrl.model("EliminarclienteCommand",{
    'DNI': fields.String(required=True, description='dni', example ="00000000T")
    })

parser = reqparse.RequestParser()
parser.add_argument("DNI", type=str)

@ClienteCtrl.route("")
class Cliente(Resource):
    @ClienteCtrl.expect(parser)
    def get(self):    
        dni = request.args.get("DNI")
        if not dni:            
            resp = make_response(jsonify({"error": "El parametro 'DNI' es obligatorio"}), 400)
            return resp
        
        dni = dni.upper()
        if not Validadores.ValidarDNI(dni):    
            resp = make_response(jsonify({"error": "El DNI introducido no es valido"}), 400)
            return resp
        # Consulta parametrizada para evitar inyecciones SQL
        query = "SELECT * FROM tbClientes WHERE DNI = ?"
        client = gestionBBDD.query_db(query, [dni], one=True)

        if client is None:    
            resp = make_response(jsonify({"error": "Cliente no encontrado"}), 404)
            return resp

        # Convierte la fila en un diccionario para devolver como JSON
        return jsonify(dict(client))
    
    @ClienteCtrl.expect(CrearclienteCommand)    
    def post(self):
        # Obtener los datos enviados en formato JSON
        data = request.get_json()

        # Validar los campos requeridos
        required_fields = ["DNI", "Nombre", "Email", "CapitalSolicitado"]
        for field in required_fields:
            if field not in data:
                resp = make_response(jsonify({"error": f"El campo '{field}' es obligatorio"}), 400)
                return resp

        # Extraer datos
        dni = data["DNI"].upper()
        nombre = data["Nombre"]
        email = data["Email"]
        capital = data["CapitalSolicitado"]
    
        if not Validadores.ValidarDNI(dni):           
            resp = make_response(jsonify({"error": "El DNI introducido no es valido"}), 400)
            return resp
        # Insertar en la base de datos
        query = """
            INSERT INTO tbClientes (DNI, Nombre, Email, CapitalSolicitado)
            VALUES (?, ?, ?, ?)
        """
        try:
            gestionBBDD.execute_query_db(query, [dni, nombre, email, capital])
            gestionBBDD.get_db().commit()  # Confirmar los cambios           
            resp = make_response(jsonify({"message": "Cliente agregado exitosamente"}), 201)
            return resp
        except Exception as e:
            resp = make_response(jsonify({"error": f"Error al agregar cliente: {str(e)}"}), 409)
            return resp
        
    @ClienteCtrl.expect(CrearclienteCommand)  
    def put(self):
        # Obtener los datos enviados en formato JSON
        data = request.get_json()

        # Validar los campos requeridos
        if "DNI" not in data:   
            resp = make_response(jsonify({"error": "El campo 'DNI' es obligatorio"}), 400)
            return resp

        # Extraer datos
        dni = data["DNI"].upper()
        nombre = data.get("Nombre")  # Puede ser opcional
        email = data.get("Email")    # Puede ser opcional
        capital = data.get("CapitalSolicitado")  # Puede ser opcional
    
        if not Validadores.ValidarDNI(dni):           
            resp = make_response(jsonify({"error": "El DNI introducido no es valido"}), 400)
            return resp

        # Construir consulta din�micamente en funci�n de los campos enviados
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
            resp = make_response(jsonify({"error": "No se proporcionaron campos para actualizar"}), 400)
            return resp

        # Agregar el DNI al final de los par�metros para la cl�usula WHERE
        params.append(dni)

        query = f"UPDATE tbClientes SET {', '.join(updates)} WHERE DNI = ?"

        try:
            rows_affected = gestionBBDD.execute_query_db(query, params)
            gestionBBDD.get_db().commit()  # Confirmar los cambios

            if rows_affected == 0:      
                resp = make_response(jsonify({"error": "Cliente no encontrado"}), 404)
                return resp
              
            resp = make_response(jsonify({"message": "Cliente actualizado exitosamente"}), 200)
            return resp
        except Exception as e:  
            resp = make_response(jsonify({"error": f"Error al actualizar cliente: {str(e)}"}), 500)
            return resp


        
    @ClienteCtrl.expect(EliminarclienteCommand)  
    def delete(self):
        # Obtener los datos enviados en formato JSON
        data = request.get_json()

        # Validar el campo obligatorio
        if "DNI" not in data:
            resp = make_response(jsonify({"error": "El campo 'DNI' es obligatorio"}), 400)
            return resp

        dni = data["DNI"].upper()
        if not Validadores.ValidarDNI(dni):           
            resp = make_response(jsonify({"error": "El DNI introducido no es valido"}), 400)
            return resp

        # Eliminar el cliente
        query = "DELETE FROM tbClientes WHERE DNI = ?"
        query2 = "DELETE FROM tbSimulaciones WHERE DNI = ?"

        try:
            rows_affected = gestionBBDD.execute_query_db(query, [dni])
            rows_affected2 = gestionBBDD.execute_query_db(query2, [dni])
            gestionBBDD.get_db().commit()  # Confirmar los cambios

            if rows_affected == 0:        
                resp = make_response(jsonify({"error": "Cliente no encontrado"}), 404)
                return resp

              
            resp = make_response(jsonify({"message": "Cliente eliminado exitosamente"}), 200)
            return resp
        except Exception as e:
            resp = make_response(jsonify({"error": f"Error al eliminar cliente: {str(e)}"}), 500)
            return resp
