from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# pylint: disable=no-member


class User(AbstractUser):
    # IMPORTANT!!!
    # If we create this class in the middle of the development, we're going to get the following error.
    # Migration admin.0001_initial is applied before its dependency core.0001_initial on database 'default'.
    #
    # To solve the error, we need to recreate the whole database and run migrations from scratch.
    # So, the better approach, when you're starting a new project, create this model right away with the blank body
    #
    # pass
    email = models.EmailField(unique=True)
