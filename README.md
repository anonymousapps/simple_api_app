# A simple api app

## Introduction

A simple API app using Python and Django using Postgres. I used Ubuntu and VSCode for development.

## Requirements

Django needs to be installed locally for development. See:
https://docs.djangoproject.com/en/5.2/topics/install/

There is a requirements.txt file in the base directory of the project for additional dependencies added.

I am using python-decouple to seperate out configs into a .env file so they aren't in the tracked settings file:

```
pip install python-decouple
```

An example of a .env file:

```
DEBUG=True
SECRET_KEY='django-insecure-2$jm=82*r#^p0-b8+0ukno+4!a798awx53rqi!z)h*8*pojr96'

DB_NAME='tasks'
DB_USER='postgres'
DB_PASSWORD='postgres'
DB_HOST='localhost'
DB_PORT='5432'
```

### Postgres

Some basic setup instructions follow.

Install Postgres:

```
sudo apt update
sudo apt install postgresql postgresql-contrib
```

To check its working you can run:

```
sudo -u postgres psql
```

then \q to exit.

To use the Postgres with Python we need an additional package:
https://www.psycopg.org/psycopg3/docs/basic/install.html

Add a database caslled 'tasks' in Postgres then run:

```
python manage.py makemigrations simple_api_app
python manage.py migrate
```

to apply the database schema.

## Virtual environment

Although not essential its a good way of seperating out projects.

To install:

```
sudo apt install python3.10-venv
```

To enter the virual environment:

```
source ~/django-env/bin/activate
```

## Running the app and tests

To run the server:

```
python manage.py runserver
```

then go to http://127.0.0.1:8000/simpleapi/

To run the tests:

```
python manage.py test simple_api_app
```

## Features of the simple api app

- Add/Edit/Delete of tasks
-
