#!/bin/bash

SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
DB_PASSWORD=$(python -c "from django.utils.crypto import get_random_string; print(get_random_string(16))")

INFO='\033[1;32m'
ENDINFO='\033[0m'

if [ $1 == 'production' ]; then
    echo -e "${INFO}Starting production server${ENDINFO}"

    echo -e "${INFO}Generating docker/.env file${ENDINFO}"
    echo "DJANGO_DEBUG=0
    DJANGO_SECRET_KEY=${SECRET_KEY}
    POSTGRES_DB=codeo
    POSTGRES_USER=codeo_app
    POSTGRES_PASSWORD=${DB_PASSWORD}
    POSTGRES_HOST=postgres
    REDIS_HOST=redis" > docker/.env

    echo -e "${INFO}Building docker container${ENDINFO}"
    docker-compose up --remove-orphans --build -d

elif [ $1 == 'debug' ]; then
    echo -e "${INFO}Starting debug server${ENDINFO}"

    echo -e "${INFO}Exporting env variables${ENDINFO}"
    export DJANGO_DEBUG=1
    export DJANGO_SECRET_KEY=${SECRET_KEY}
    export POSTGRES_DB=codeo
    export POSTGRES_USER=codeo_app
    export POSTGRES_PASSWORD=${DB_PASSWORD}
    export POSTGRES_HOST=localhost
    export REDIS_HOST=localhost

    echo -e "${INFO}Installing python requirements${ENDINFO}"
    pip install --upgrade pip && pip install -r requirements.txt

    echo -e "${INFO}Starting postgresql server${ENDINFO}"
    systemctl start postgresql.service
    sudo -u postgres createuser codeo_app
    sudo -u postgres createdb codeo

    echo -e "${INFO}Starting redis server${ENDINFO}"
    docker run -p 6379:6379 -d redis:latest

    echo -e "${INFO}Apply migrations${ENDINFO}"
    python manage.py migrate

    echo -e "${INFO}Starting django server${ENDINFO}"
    python manage.py runserver 0.0.0.0:8000
fi