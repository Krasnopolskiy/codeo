# codeshare
## Installation
1. Clone repository:
    ```bash
    git clone https://github.com/Krasnopolskiy/codeshare.git
    cd codeshare
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
4. Generate secret key (python shell):
    ```python
    from django.core.management.utils import get_random_secret_key  
    with open('secretkey.txt', 'w') as f:
        f.write(get_random_secret_key())
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
