===============================================================================
Howto Django
===============================================================================

Install django
-------------------------------------------------------------------------------
pip install django
pip install django-extensions

Install django on windows using anaconda
-------------------------------------------------------------------------------
conda install django
conda install -c https://conda.anaconda.org/ioos django-extensions

add  to settings.py
INSTALLED_APPS = (
    'django_extensions',
)

Setup project
-------------------------------------------------------------------------------
1. django-admin.py startproject www
2. edit settings.py
3. python manage.py syncdb
4. create superuser superuser/superuser

Commands
-------------------------------------------------------------------------------
python manage.py show_urls
--> Shows all rendered urls within the django application

python manage.py runserver
--> Start local development server


