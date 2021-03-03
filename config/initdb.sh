#/bin/bash
python manage.py wait_for_db &&
python manage.py migrate &&
python manage.py ensure_adminuser --username=$DJANGO_SUPERUSER_USERNAME \
                                  --email=$DJANGO_SUPERUSER_EMAL \
                                  --password=$DJANGO_SUPERUSER_PASSWORD
