from BBDD import gestionBBDD

class ClienteRepository:
    @staticmethod
    def get_by_dni(dni):
        query = "SELECT * FROM tbClientes WHERE DNI = ?"
        return gestionBBDD.query_db(query, [dni], one=True)

    @staticmethod
    def create(dni, nombre, email, capital):
        query = """
            INSERT INTO tbClientes (DNI, Nombre, Email, CapitalSolicitado)
            VALUES (?, ?, ?, ?)
        """
        gestionBBDD.execute_query_db(query, [dni, nombre, email, capital])
        gestionBBDD.get_db().commit()

    @staticmethod
    def update(dni, nombre=None, email=None, capital=None):
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
            return 0

        params.append(dni)
        query = f"UPDATE tbClientes SET {', '.join(updates)} WHERE DNI = ?"
        
        rows_affected = gestionBBDD.execute_query_db(query, params)
        gestionBBDD.get_db().commit()
        return rows_affected

    @staticmethod
    def delete(dni):
        # Nota: La logica original tambien borraba simulaciones.
        # ¿Deberia esto estar aqui o en un servicio?
        # Por ahora mantenemos la logica intacta del controlador original, 
        # pero idealmente el borrado en cascada deberia ser gestionado por la BBDD o un servicio.
        # Aquí proveemos metodos atomicos. El controlador o servicio puede llamar a ambos.
        query = "DELETE FROM tbClientes WHERE DNI = ?"
        rows_affected = gestionBBDD.execute_query_db(query, [dni])
        gestionBBDD.get_db().commit()
        return rows_affected
