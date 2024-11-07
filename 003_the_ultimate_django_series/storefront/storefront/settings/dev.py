from .common import *  # pylint: disable=relative-beyond-top-level


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-c$3_aqa0_v4@hg^peoj_uww1#p^vf4*co(x820$(rv$g1^1oc+"


if DEBUG:
    MIDDLEWARE += [  # pylint: disable=undefined-variable
        "silk.middleware.SilkyMiddleware"
    ]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "storefront",
        "HOST": "mysql",
        "USER": "root",
        "PASSWORD": "",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp4dev"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = "from@example.com"


CELERY_BROKER_URL = "redis://redis:6379/1"
CELERY_BEAT_SCHEDULE = {
    "notify_customers": {
        "task": "playground.tasks.notify_customers",
        # "schedule": crontab(day_of_week=1, hour=7, minute=30),
        # "schedule": crontab(minute="*/15"),
        "schedule": 5,  # 5 seconds
        "args": ["Hello world"],
    },
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/2",
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}
