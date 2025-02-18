#!/bin/sh

echo "Esperando a que MySQL esté listo..."
while ! mysqladmin ping -h"$MYSQL_HOST" --silent; do
    sleep 1
done

echo "Aplicando migraciones..."
python manage.py migrate

echo "Cargando datos iniciales..."
python manage.py loaddata fixtures/fixtures.json || echo "No se pudo cargar el fixture"

echo "Iniciando aplicación..."
exec "$@"
