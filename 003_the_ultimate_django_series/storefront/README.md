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
