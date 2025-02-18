#!/bin/bash

while ! nc -z db 3306; do
  sleep 1
done

python manage.py migrate || { echo "ERROR: No se pudieron aplicar las migraciones."; exit 1; }


if python manage.py loaddata fixtures.json; then
    echo "Fixtures cargados correctamente."
else
    echo "No se pudieron cargar los fixtures, verificando si ya existen los datos..."
fi


mkdir -p /app/static /app/staticfiles
chmod -R 755 /app/static /app/staticfiles

python manage.py collectstatic --noinput --clear

if [ "$(ls -A /app/staticfiles)" ]; then
    echo "Archivos estáticos recolectados correctamente."
else
    echo "ERROR: No se recolectaron archivos estáticos."
    exit 1
fi

export DJANGO_SETTINGS_MODULE=config.settings 
python manage.py runserver 0.0.0.0:8000 & 


if [ "$CREATE_SUPERUSER" = "true" ]; then
    echo "Creando superusuario..."
    python manage.py createsuperuser --noinput || echo "No se pudo crear el superusuario."
fi


exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers=4 --log-level=info --timeout 120
