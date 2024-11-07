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
        "HOST": "localhost",
        "USER": "root",
        "PASSWORD": "",
    }
}
