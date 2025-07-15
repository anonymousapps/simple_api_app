# A simple api app

## Introduction

A simple API app using Python and Django using Postgres. I used Ubuntu and VSCode for development.

This app enables the adding of a tasks with the fields:
title
description
status
due date

The status is a defined set of values stored on the database.

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

## REST API

A REST API has been implemented using [Django REST Framework](https://www.django-rest-framework.org/).

This enables intereacting with the Status and Task data via an API. For example:

http://127.0.0.1:8000/api - The API root

http://127.0.0.1:8000/api/status/ - shows all statuses
http://127.0.0.1:8000/api/status/2/ - shows the status with id 2

http://127.0.0.1:8000/api/tasks/ - shows all tasks
http://127.0.0.1:8000/api/tasks/1/ - shows the task with id 1

Using a curl request we may use something like this to get all the tasks in json format:

```
curl -u rgidding -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/api/tasks/
```

Further improvements could be made for [permissions](https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/), for allowing more curl requests and updates etc from only specific users.

## Features of the simple api app

- Add/Edit/Delete of tasks using front-end via http://127.0.0.1:8000/simpleapi/
- Add/Edit/Delete of status and tasks using rest api via http://127.0.0.1:8000/api/
