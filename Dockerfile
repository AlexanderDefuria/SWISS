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

ARG DJANGO_SECRET_KEY
ARG DB_ENGINE
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG DB_SSLMODE
RUN echo "$DJANGO_SECRET_KEY"
RUN echo "$DB_ENGINE"
RUN echo "$DB_NAME"
RUN echo $DB_USER
RUN echo $DB_PASSWORD
RUN echo $DB_HOST
RUN echo $DB_PORT
RUN echo $DB_SSLMODE
RUN set -ex \
    && { \
        printf '{\n\t"SECRET_KEY": "%s",\n' "$DJANGO_SECRET_KEY"; \
        printf '\t"ENGINE": "%s",\n' "$DB_ENGINE"; \
        printf '\t"NAME": "%s",\n' "$DB_NAME"; \
        printf '\t"USER": "%s",\n' "$DB_USER"; \
        printf '\t"PASSWORD": "%s",\n' "$DB_PASSWORD"; \
        printf '\t"HOST": "%s",\n' "$DB_HOST"; \
        printf '\t"PORT": "%s",\n' "$DB_PORT"; \
        printf '\t"sslmode":"%s" \n' "$DB_SSLMODE"; \
        printf '\n\n}'; \
    } > secrets.json



EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "FRC-Scouting.wsgi"]





