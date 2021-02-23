# codeo
## Installation
1. Clone repository:
    ```bash
    git clone https://github.com/Krasnopolskiy/codeo.git
    cd codeo
    ```
2. Create virtual environment:
    ```bash
    python3 -m venv venv
    ```
3. Activate virual environment:
   - Linux:
        ```bash
        source venv/bin/activate
        ```
   - Windows:
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
4. Upgrade pip to the latest version:
    ```bash
    python3 -m pip install --upgrade pip
    ```
5. Install django:
    ```bash
    python3 -m pip install django
    ```
6. Generate app secret key:
    ```bash
    python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```
7. Generate postgres and superuser password:
    ```bash
    python3 -c "from django.utils.crypto import get_random_string; print(get_random_string(16))"
    ```
8. Create `./config/.env`:
    ```
    DJANGO_DEBUG=
    DJANGO_SECRET_KEY="<secret_key>"
    DJANGO_SUPERUSER_USERNAME=admin
    DJANGO_SUPERUSER_EMAIL=codeomain@gmail.com
    DJANGO_SUPERUSER_PASSWORD=<password>
    POSTGRES_DB=codeo
    POSTGRES_USER=codeo_app
    POSTGRES_PASSWORD=<password>
    POSTGRES_HOST=
    REDIS_HOST=
    ```
    For development:
    ```
    DJANGO_DEBUG=TRUE
    POSTGRES_HOST=localhost
    REDIS_HOST=localhost
    ```
    For production:
    ```
    DJANGO_DEBUG=FALSE
    POSTGRES_HOST=postgres
    REDIS_HOST=redis
    ```
9.  Export environment variables:
    - Linux:
        ```bash
        source ./config/.env
        ```
    - Windows:
        ```powershell
        .\config\Source.ps1
        ```
## Run development server
1. Run postgres server:
   - Linux:
        ```bash
        docker run -e POSTGRES_USER=$POSTGRES_USER -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -e POSTGRES_DB=$POSTGRES_DB -p 5432:5432 -d postgres
        ```
   - Windows:
        ```powershell
        docker run -e POSTGRES_USER=$env:POSTGRES_USER -e POSTGRES_PASSWORD=$env:POSTGRES_PASSWORD -e POSTGRES_DB=$env:POSTGRES_DB -p 5432:5432 -d postgres
        ```
2. Run redis server:
    ```bash
    docker run -p 6379:6379 -d redis
    ```
3. Install requirements:
    ```bash
    python3 -m pip install -r requirements.txt
    ```
4. Apply migrations:
    ```bash
    python3 manage.py migrate
    ```
5. Collect static files:
    ```bash
    python3 manage.py collectstatic --noinput
    ```
6. Create superuser:
    ```bash
    python3 manage.py createsuperuser --noinput
    ```
7. Run django server:
    ```bash
    python3 manage.py runserver 0.0.0.0:8000
    ```
## Run production server
```bash
docker-compose up --build -d
```
