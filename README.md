# codeo
## Installation
1. Clone repository:
    ```bash
    git clone https://github.com/Krasnopolskiy/codeo.git
    cd codeo
    ```
2. Create and activate virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
4. Generate secret key:
    ```bash
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' > secretkey.txt
    ```
5. Apply migrations:
    ```bash
    python manage.py migrate
    ```

## Run service
1. Run redis server:
    ```bash
    docker run -p 6379:6379 -d redis:5
    ```
2. Run django server:
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```
