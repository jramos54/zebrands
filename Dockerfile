FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
COPY . .

RUN chmod +x /app/entrypoint.sh

ARG DJANGO_SETTINGS_MODULE=config.settings
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
ENV PYTHONUNBUFFERED=1

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
