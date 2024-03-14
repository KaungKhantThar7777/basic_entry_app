from django.shortcuts import render
from .models import Topic

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