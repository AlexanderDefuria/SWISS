FROM python:3.9.10-buster

WORKDIR /usr/share/FRC-Scouting

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD ./ /usr/share/FRC-Scouting/

RUN set -ex \
    && apt-get update \
    && apt-get install -y libpq-dev \
    && apt-get install -y nginx \
    && apt-get install -y python3-venv \
    && python3 -m venv ./venv \
    && ./venv/bin/pip3 install -r requirements.txt

ADD ./FRC-Scouting.nginx /etc/nginx/sites-available/FRC-Scouting
RUN set -ex \
    && ln -s /etc/nginx/sites-available/FRC-Scouting /etc/nginx/sites-enabled

ENV VIRTUAL_ENV ./venv
ENV PATH ./venv/bin:$PATH

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "FRC-Scouting.wsgi"]





