from django.shortcuts import render, redirect
from .models import Topic
from .forms import TopicForm


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