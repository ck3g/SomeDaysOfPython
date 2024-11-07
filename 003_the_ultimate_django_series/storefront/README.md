# Storefront app

## Virtual env

```
pipenv intall django
```

Use `pipenv --venv` to see environment location

### Launch the environment

```
pipenv shell
```

### Create the project

```
django-admin startproject storefront .
```

### Run fake SMTP server

```
docker run --rm -it -p 3000:80 -p 2525:25 rnwood/smtp4dev
```

### Run redis

```
docker run -d -p 6379:6379 redis
```

### Run celery worker

```
celery -A storefront worker --loglevel=info
```

### Run celery beat

It needs to be run together with celery worker

```
celery -A storefront beat
```

### Run celery flower

```
celery -A storefront flower
```

### Using pytest-watch

```
ptw
```

### Collect static files

Collects all the static files from all the apps and stores them into STATIC_ROOT folder. Sort of bundling assets I assume.

```
python manage.py collectstatic
```

### Start gunicorn

If running on development environment, gunicorn will not pick any new changes in the files. Use dev server for that.

```
gunicorn storefront.wsgi
```

### Docker

#### Run in background

```
docker-compose run -d
```

#### Check tests

```
docker-compose logs tests
```

#### Watch tests

```
docker-compose logs -f tests
```

#### Run bash

```
docker-compose run web bash
```

#### Seed

```
docker-compose run web python manage.py seed_db
```
