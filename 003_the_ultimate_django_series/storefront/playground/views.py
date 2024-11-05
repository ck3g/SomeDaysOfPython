from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from store.models import Product
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers


def say_hello(request):
    return render(request, "hello.html", {"name": "John"})


def products(request):
    query_set = Product.objects.filter(  # pylint: disable=no-member
        title__icontains="coffee"
    )

    return render(request, "hello.html", {"name": "John", "products": list(query_set)})


def send_emails(request):
    try:
        # one way
        # send_mail("subject", "message", "test@example.com", ["john@doe.com"])

        # another way
        message = EmailMessage(
            "subject", "message", "test@example.com", ["john@doe.com"]
        )
        message.attach_file("playground/static/test-attachment.txt")
        message.send()
    except BadHeaderError:
        return HttpResponse("Bad Header Error")

    return HttpResponse("Emails has been sent")


def send_templated_emails(request):
    try:
        message = BaseEmailMessage(
            template_name="emails/hello.html",
            context={"name": "John Doe"},
        )
        message.send(to=["jonh@doe.com"])
    except BadHeaderError:
        return HttpResponse("Bad Header Error")

    return HttpResponse("Emails has been sent")


def send_admins_emails(request):
    try:
        mail_admins("subject", "message", html_message="<h2>message</h2>")
    except BadHeaderError:
        return HttpResponse("Bad Header Error")

    return HttpResponse("Emails has been sent")


def background_task(request):
    notify_customers.delay("Hello")
    return HttpResponse("Background task has been triggered")
