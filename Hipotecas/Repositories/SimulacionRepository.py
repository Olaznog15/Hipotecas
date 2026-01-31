from BBDD import gestionBBDD
from datetime import datetime

class SimulacionRepository:
    @staticmethod
    def create(dni, capital, tae, plazo, cuota, importe_total):
        query = """
            INSERT INTO tbSimulaciones (DNI, Capital, Tae, Plazo, CuotaMensual, ImporteTotal, FechaSimulacion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        gestionBBDD.execute_query_db(query, [dni, capital, tae, plazo, cuota, importe_total, datetime.now()])
        gestionBBDD.get_db().commit()

    @staticmethod
    def delete_by_client_dni(dni):
        query = "DELETE FROM tbSimulaciones WHERE DNI = ?"
        rows_affected = gestionBBDD.execute_query_db(query, [dni])
        gestionBBDD.get_db().commit()
        return rows_affected
