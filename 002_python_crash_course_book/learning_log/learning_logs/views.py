from django.shortcuts import render, redirect

# Create your views here.

from .models import Topic
from .forms import TopicForm


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


def new_topic(request):
    """Add a new topic"""
    if request.method != "POST":
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted, process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topics")

    # Display a blank or invalid form
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)
