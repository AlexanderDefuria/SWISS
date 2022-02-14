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
    && ln -s /etc/nginx/sites-available/FRC-Scouting /etc/nginx/sites-enabled
    
RUN     

ENV VIRTUAL_ENV ./venv
ENV PATH ./venv/bin:$PATH

RUN set -ex \
    && { \
        printf '{\n\t"SECRET_KEY": "%s",\n' "$DJANGO_SECRET_KEY"; \
        printf '\t"ENGINE": "django.db.backends.postgresql_psycopg2",\n'; \
        printf '\t"NAME": "swissdbdev",\n'; \
        printf '\t"USER": "swiss",\n'; \
        printf '\t"PASSWORD": "l5oix3lgmz0p5gzp",\n'; \
        printf '\t"HOST": "db-postgresql-nyc3-00259-do-user-7775406-0.b.db.ondigitalocean.com",\n'; \
        printf '\t"PORT": "25060",\n'; \
        printf '\t"sslmode": "require"\n'; \
        printf '\n\n}'; \
    } > secrets.json


EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "FRC-Scouting.wsgi"]





