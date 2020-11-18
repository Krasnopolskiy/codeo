# codeshare
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd codeshare
mkdir sources
echo '{secretkey}' > secretkey.txt
python manage.py makemigrations
python manage.py migrate
docker run -p 6379:6379 -d redis:5
python manage.py runserver
```
