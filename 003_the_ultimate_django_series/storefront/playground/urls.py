from django.urls import path
from . import views


urlpatterns = [
    path("hello/", views.say_hello),
    path("products/", views.products),
    path("send_emails/", views.send_emails),
    path("send_admins_emails/", views.send_admins_emails),
]
