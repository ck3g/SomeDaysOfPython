from django.shortcuts import render, redirect

# Create your views here.

from .models import Topic
from .forms import TopicForm, EntryForm


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


def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)  # pylint: disable=no-member

    if request.method != "POST":
        # No data submitted; create a blank form
        form = EntryForm()
    else:
        # POST data submitted; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    # Display a blank or invalid form
    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)
