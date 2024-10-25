from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product


def say_hello(request):
    return render(request, "hello.html", {"name": "John"})


def products(request):
    query_set = Product.objects.filter(  # pylint: disable=no-member
        title__icontains="coffee"
    )

    return render(request, "hello.html", {"name": "John", "products": list(query_set)})
