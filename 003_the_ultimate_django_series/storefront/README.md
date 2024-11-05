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
