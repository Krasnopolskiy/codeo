# codeshare
## Installation
```
git clone https://github.com/Krasnopolskiy/codeshare.git
cd codeshare
git checkout dev
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd codeshare
mkdir sources
echo '{secretkey}' > secretkey.txt
python manage.py makemigrations api
python manage.py migrate
```

## Run service
```
docker run -p 6379:6379 -d redis:5
python manage.py runserver
```
Run in local network
`python manage.py runserver 0.0.0.0:8000`
