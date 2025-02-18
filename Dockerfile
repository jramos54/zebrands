FROM python:3.12

WORKDIR /app

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
COPY . .

# Configuración del entorno
ARG DJANGO_SETTINGS_MODULE=config.settings
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
ENV PYTHONUNBUFFERED=1

# Ejecutar migraciones y cargar fixtures
RUN python manage.py migrate && \
    python manage.py loaddata fixtures/fixtures.json || echo "No se pudo cargar el fixture"

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=4"]
