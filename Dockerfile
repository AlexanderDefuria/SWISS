FROM python:3.9.10-buster

WORKDIR /usr/share/FRC-Scouting

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD ./ /usr/share/FRC-Scouting/

RUN set -ex \
    && apt-get update \
    && apt-get install -y libpq-dev \
    && apt-get install -y nginx \
    && python3 -m venv --copies ./venv \
    && ./venv/bin/pip3 install -r requirements.txt

ADD ./FRC-Scouting.nginx /etc/nginx/sites-available/FRC-Scouting
RUN set -ex \
    && ln -s /etc/nginx/sites-available/FRC-Scouting /etc/nginx/sites-enabled \
    && echo "STATIC_ROOT = os.path.join(BASE_DIR, 'static')" >> ./FRC-Scouting/settings.py

ENV VIRTUAL_ENV ./venv
ENV PATH ./venv/bin:$PATH

ARG DJANGO_SECRET_KEY
ARG DB_ENGINE
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG DB_SSLMODE
ARG AWS_ACCESS_KEY_ID
ARG AWS_LOCATION
ARG AWS_S3_ENDPOINT_URL
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_STORAGE_BUCKET_NAME


RUN set -ex \
    && { \
        printf '{\n\t"SECRET_KEY": "%s",\n' "$DJANGO_SECRET_KEY"; \
        printf '\t"ENGINE": "%s",\n' "$DB_ENGINE"; \
        printf '\t"NAME": "%s",\n' "$DB_NAME"; \
        printf '\t"USER": "%s",\n' "$DB_USER"; \
        printf '\t"PASSWORD": "%s",\n' "$DB_PASSWORD"; \
        printf '\t"HOST": "%s",\n' "$DB_HOST"; \
        printf '\t"PORT": "%s",\n' "$DB_PORT"; \
        printf '\t"sslmode":"%s", \n' "$DB_SSLMODE"; \
        printf '\t""AWS_ACCESS_KEY_ID": "%s",\n' "$AWS_ACCESS_KEY_ID"; \
        printf '\t""AWS_LOCATION" : "%s",\n' "$AWS_LOCATION"; \
        printf '\t""AWS_S3_ENDPOINT_URL" : "%s",\n' "$AWS_S3_ENDPOINT_URL"; \
        printf '\t""AWS_SECRET_ACCESS_KEY" : "%s",\n' "$AWS_SECRET_ACCESS_KEY"; \
        printf '\t""AWS_STORAGE_BUCKET_NAME" : "%s"\n' "$AWS_STORAGE_BUCKET_NAME"; \
        printf '\n\n}'; \
    } > secrets.json



EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "FRC-Scouting.wsgi"]





