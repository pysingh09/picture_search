# Picture Search

## Python version

    python 3.8

## Django version

    Django==3.1.7

## Database

    sqlite3

## Other Packages

    flickrapi==2.4.0
    reverse-geocoder==1.5.1

# Commands to Execute before accessing

### Install all the dependencies required to run the project

    pip install -r requirements.txt

### To generate desired migrations files of created folder

    python manage.py makemigrations

### To apply generated migration to DB

    python manage.py migrate 

### Create user to perform search

    python manage.py createsuperuser
    Exxample:- username: admin, email: admin@gmail.com, password: admin

## References:-

    https://www.flickr.com/services/api/flickr.photos.search.html
    https://pypi.org/project/reverse_geocoder/

## To Run the Project:-
    http://127.0.0.1:8000/ --> dummy credentials:- username=admin, password=admin
    http://127.0.0.1:8000/home/ --> search images with provided latitude, longitude
    http://127.0.0.1:8000/favorite-images/ --> Get your favorite images list 