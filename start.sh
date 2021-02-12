#!/bin/bash

INFO='\033[1;32m'
ENDINFO='\033[0m'

echo -e "${INFO}Updating pip and installing django${ENDINFO}"
python -m pip install --upgrade pip && python -m pip install django
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
DB_PASSWORD=$(python -c "from django.utils.crypto import get_random_string; print(get_random_string(16))")

if [ $1 == 'production' ]; then
    echo -e "${INFO}Starting production server${ENDINFO}"

    echo -e "${INFO}Generating docker/.env file${ENDINFO}"
    echo "DJANGO_DEBUG=0" > docker/.env
    echo "DJANGO_SECRET_KEY=${SECRET_KEY}" >> docker/.env
    echo "POSTGRES_DB=codeo" >> docker/.env
    echo "POSTGRES_USER=codeo_app" >> docker/.env
    echo "POSTGRES_PASSWORD=${DB_PASSWORD}" >> docker/.env
    echo "POSTGRES_HOST=postgres" >> docker/.env
    echo "REDIS_HOST=redis" >> docker/.env

    echo -e "${INFO}Building docker container${ENDINFO}"
    docker-compose up --remove-orphans --build

elif [ $1 == 'development' ]; then
    echo -e "${INFO}Starting development server${ENDINFO}"

    echo -e "${INFO}Exporting env variables${ENDINFO}"
    export DJANGO_DEBUG=1
    export DJANGO_SECRET_KEY=secret
    export POSTGRES_DB=codeo
    export POSTGRES_USER=codeo_app
    export POSTGRES_PASSWORD=password
    export POSTGRES_HOST=localhost
    export REDIS_HOST=localhost

    echo -e "${INFO}Installing python requirements${ENDINFO}"
    python -m pip install --upgrade pip \
        && python -m pip install -r requirements.txt

    echo -e "${INFO}Starting postgresql server${ENDINFO}"
    systemctl start postgresql.service
    sudo -u postgres createuser $POSTGRES_USER
    sudo -u postgres createdb codeo

    echo -e "${INFO}Starting redis server${ENDINFO}"
    docker run -p 6379:6379 -d redis:latest

    echo -e "${INFO}Apply migrations${ENDINFO}"
    python manage.py migrate

    echo -e "${INFO}Starting django server${ENDINFO}"
    python manage.py runserver 0.0.0.0:8000
fi