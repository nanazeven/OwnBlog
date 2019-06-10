python manage.py makemigrations && python manage.py migrate && gunicorn django_blog.wsgi:application -c gunicorn.conf
