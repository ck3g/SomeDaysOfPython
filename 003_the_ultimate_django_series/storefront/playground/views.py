from django.core.cache import cache
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from store.models import Product
from templated_mail.mail import BaseEmailMessage
import requests
import logging
from .tasks import notify_customers

logger = logging.getLogger(__name__)


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


def slow_endpoint(request):
    key = "httpbin_result"
    if cache.get(key) is None:
        response = requests.get("https://httpbin.org/delay/2")
        data = response.json()
        cache.set(key, data)

    return JsonResponse(cache.get(key))


@cache_page(5 * 60)  # uses function name as a cache key
def slow_endpoint_decorated(request):
    response = requests.get("https://httpbin.org/delay/2")
    data = response.json()
    return JsonResponse(data)


class CachedView(APIView):
    @method_decorator(cache_page(5 * 60))
    def get(self, request):
        response = requests.get("https://httpbin.org/delay/2")
        data = response.json()
        return JsonResponse(data)


class LoggingView(APIView):
    def get(self, request):
        try:
            logger.info("Calling httpbin")
            response = requests.get("https://httpbin.org/delay/1")
            logger.info("Received the response")
            data = response.json()
        except requests.ConnectionError:
            logger.critical("httpbin is offlines")

        return JsonResponse(data)
