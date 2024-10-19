# Learning Log

A web app called Learning Log that allows users to
log the topics they're interested in and make journal entries as
they learn about each topic. The Learning Log home have describes
the site and invite users to either register or log in. Once
logged in, a user can create new topics, add new entries, and read
and edit existing entries.

## Virtual Environment

### Create a Virtual Environment

```
python -m venv ll_env
```

### Activate the environment

```
source ll_env/bin/activate
```

### Deactivate the envrionment

```
deactivate
```


## Installing Django

```
pip install --upgrade pip
pip install django
```


## Creating a Project in Django

```
django-admin startproject ll_project .
```


## Creating a database

```
python manage.py migrate
```

## Run the server

```
python manage.py runserver
```

## Starting an app

```
source ll_env/bin/activate
python manage.py startapp learning_logs
```