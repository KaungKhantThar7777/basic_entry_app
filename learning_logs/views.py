from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm,EntryForm


# Create your views here.
def index(request):
    # The homepage for learning log
    return render(request, 'learning_logs/index.html')


def topics(request):
    # Show all topics
    topics_data = Topic.objects.order_by('date_added')
    context = {'topics': topics_data}

    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Show single topic and all entries"""
    topic_data = Topic.objects.get(id=topic_id)
    entries = topic_data.entry_set.order_by('-date_added')
    context = {'topic': topic_data, 'entries': entries}

    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    """Add a new topic"""
    if request.method != "POST":
        # No data submitted; create a blank form
        form  = TopicForm()
    else: 
        # POST data submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    
    context = {'form':form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    """Add a new entry"""
    topic_data = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        # No date submitted, createa blank form
        form = EntryForm()
    else:
        # POST data submitted; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry_data = form.save(commit=False)
            new_entry_data.topic = topic_data
            new_entry_data.save()
            return redirect('learning_logs:topic', topic_id= topic_id)
    # Display a blank form or invalid form
    context = {'topic': topic_data, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    """Edit on exiting entry"""
    entry_data = Entry.objects.get(id=entry_id)
    topic_data = entry_data.topic

    if request.method != 'POST':
        # Initial request; pre-fill form with current entry
        form = EntryForm(instance=entry_data)
    else:
        # POST form submitted; process data
        form = EntryForm(instance=entry_data, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic_data.id)
    context = {'entry':entry_data, 'topic': topic_data, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)