# imdb-django-rest-framewrok
use with store procedure
# Please follow the process below to install
1. Clone this repository (https://github.com/Exclusive-888/imdb-django-rest-framewrok.git)
# Setting up a development virtual environment
2.start  environment with requirements e.g. pip install -r requirements.txt
# migrating the already defined models
3.python manage.py migrate
# super user create before the dummy json data be load
4.python manage.py createsuperuser
# loading dummy json data
5.python manage.py loaddata data.json
# collectstatic required/need for ckeditor 
6.python manage.py collectstatic
# now Finallyy
7. python manage.py runserver
# api-view for movies(for admin login must be required)
8. http://127.0.0.1:8000/api/movie/








