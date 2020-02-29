from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
    """The home page for django app."""
    return render(request, 'django_apps/index.html')


@login_required()
def topics(request):
    """Show all topic"""
    topics_list = Topic.objects.filter(owner=request.user).order_by(
        'date_added')
    context = {'topics_list': topics_list}
    return render(request, 'django_apps/topics.html', context)


@login_required()
def topic(request, topic_id):
    """Get topic and all entries associated with it."""
    topic = get_object_or_404(Topic, id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'django_apps/topic.html', context)


@login_required()
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()

    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            n_topic = form.save(commit=False)
            n_topic.owner = request.user
            n_topic.save()
            return redirect('django_apps:topics')

    # Display a blank name or invalid form.
    context = {'form': form}
    return render(request, 'django_apps/new_topic.html', context)


@login_required()
def new_entry(request, topic_id):
    """Add a new entry for a topic."""
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # NO data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            latest_entry = form.save(commit=False)
            latest_entry.topic = topic
            latest_entry.save()
            return redirect('django_apps:topic', topic_id=topic_id)

    # Display a blank name or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'django_apps/new_entry.html', context)


@login_required()
def edit_entry(request, entry_id):
    """Allows the user to edit an entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    # Make sure the account belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('django_apps:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'django_apps/edit_entry.html', context)
