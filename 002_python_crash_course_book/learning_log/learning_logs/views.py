from django.shortcuts import render

# Create your views here.

from .models import Topic


def index(request):
    """The home page for Learning Log."""
    return render(request, "learning_logs/index.html")


def topics(request):
    """Show all topics"""
    all_topics = Topic.objects.order_by("date_added")  # pylint: disable=no-member
    context = {"topics": all_topics}
    return render(request, "learning_logs/topics.html", context)


def topic(request, topic_id):
    """Show a single topic and all its entries"""
    one_topic = Topic.objects.get(id=topic_id)  # pylint: disable=no-member
    entries = one_topic.entry_set.order_by("-date_added")
    context = {"topic": one_topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)
