from django.urls import path
from . import views


urlpatterns = [
    path("hello/", views.say_hello),
    path("products/", views.products),
    path("send_emails/", views.send_emails),
    path("send_templated_emails/", views.send_templated_emails),
    path("send_admins_emails/", views.send_admins_emails),
    path("background_task/", views.background_task),
    path("slow_endpoint/", views.slow_endpoint),
]
