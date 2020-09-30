# codeshare
```
python -m venv venv
source venv/bin/activate
pip install Django
pip install djangorestframework
pip install django-crispy-forms
cd codeshare
mkdir sources
echo '{secretkey}' > secretkey.txt
python manage.py makemigrations api
python manage.py makemigrations notes
python manage.py migrate
python manage.py runserver
```
