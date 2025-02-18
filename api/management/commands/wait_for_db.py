import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Comando para esperar que la base de datos esté lista"""

    def handle(self, *args, **kwargs):
        self.stdout.write("Esperando a la base de datos...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write("Base de datos no disponible, reintentando en 5 segundos...")
                time.sleep(5)

        self.stdout.write(self.style.SUCCESS("Base de datos disponible. Continuando..."))
