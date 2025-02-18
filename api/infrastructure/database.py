import os
from django.db import connections

def get_db_connection():
    """Devuelve la conexión activa a la base de datos."""
    db_conn = connections['default']
    try:
        db_conn.ensure_connection()
        return db_conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
