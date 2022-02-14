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
        printf '{\n\t"SECRET_KEY": "$DJANGO_SECRET_KEY",\n'; \
        printf '\t"ENGINE": "$DB_ENGINE",\n'; \
        printf '\t"NAME": "$DB_NAME",\n'; \
        printf '\t"USER": "$DB_USER",\n'; \
        printf '\t"PASSWORD": "$DB_PASSWORD",\n'; \
        printf '\t"HOST": "$DB_HOST",\n'; \
        printf '\t"PORT": "$DB_PORT",\n'; \
        printf '\t"sslmode": "$DB_SSLMODE"\n'; \
        printf '\n\n}'; \
    } > secrets.json



EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "FRC-Scouting.wsgi"]





