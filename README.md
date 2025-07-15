# A simple api app

## Introduction

- An app using Python and Django using Postgres. I used Ubuntu and VSCode for development.
- This is a back-end and front-end in its own right but also exposes an API that can be used by a seperate front-end.

I have written a simple front-end in the following repository:
https://github.com/anonymousapps/api-frontend

This app enables the adding of a tasks with the fields:

- title
- description (optional)
- status
- due date

The status is a defined set of values stored on the database.

## Features of the standalone Django app

- Add/Edit/Delete of tasks using front-end via http://127.0.0.1:8000/simpleapi/
- User login so user can only See and Add/Edit/Delete their tasks
- Formatting using https://getbootstrap.com/
- Datetime picker for entering the due date
- Navigation of tasks using https://datatables.net/
- Filters out tasks that have a status of Done (this assumes we add a status of Done)
- If a date is in the past (overdue) the text is shown in red
- Web based REST API and endpoints using [Django REST framework](https://www.django-rest-framework.org/) (See [below](#rest-api) for more details)

**Possible future improvements (depending on requirements)**

- Show tasks that are Done in seperate page just as a list without Edit and Delete.
- Show tasks near due in different colour
- Add authentication to endpoints using [this guide](https://www.django-rest-framework.org/api-guide/authentication/)

## Screenshots

The task list:

![Alt text](screenshots/task_list_page.png?raw=true "The task list page")

The add task screen:

![Alt text](screenshots/add_task_page.png?raw=true "The add task page")

The edit task screen:

![Alt text](screenshots/edit_task_page.png?raw=true "The edit task page")

Delete confirmation:

![Alt text](screenshots/delete_confirmation.png?raw=true "The delete confirmation")

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

Add a database called 'tasks' in Postgres then run:

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

To add the venv:

```
python -m venv django-env
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

This enables interacting with the Status and Task data via an API in two ways:

(1) Web API

Add/Edit/Delete and viewing of tasks, statuses. E.g.

http://127.0.0.1:8000/api - The API root

http://127.0.0.1:8000/api/status/ - shows all statuses
http://127.0.0.1:8000/api/status/2/ - shows the status with id 2

http://127.0.0.1:8000/api/tasks/ - shows all tasks
http://127.0.0.1:8000/api/tasks/1/ - shows the task with id 1

The reason the Web API is seperate is to provide URLs to other parts of the Web API in the responses.

(2) Via endpoints

Get all tasks:

```
curl -X GET http://127.0.0.1:8000/api/task_list/
```

Get all statuses:

```
curl -X GET http://127.0.0.1:8000/api/statuses/
```

Add a task (description is optional):

```
curl -X POST -d 'status=2&title=API Title 2&description=API DESC 2&due_date=2025-08-30 12:04:00' http://127.0.0.1:8000/api/task_list/
```

Get a task by id:

```
curl -X GET http://127.0.0.1:8000/api/task_list/23/
```

Edit a task (status):

```
curl -X PUT -d 'status=3' http://127.0.0.1:8000/api/task_list/23/
```

Delete a task:

```
curl -X DELETE http://127.0.0.1:8000/api/task_list/23/
```
