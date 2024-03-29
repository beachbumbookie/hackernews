import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import utc
from stories.models import Story
from stories.forms import StoryForm
from django.http import HttpResponseRedirect, HttpResponse

def score(story,gravity=1.8,timebase=120):
    points = (story.points - 1)**0.8
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    age = int((now - story.created_at).total_seconds())/60

    return points/(age+timebase)**1.8

def top_stories(top=180, consider=1000):
    latest_stories = Story.objects.all().order_by('-created_at')[:consider]
    ranked_stories = sorted([(score(story),story) for story in latest_stories], reverse = True)
    return [story for _, story in ranked_stories][:top]
    
def index(request):
    stories = top_stories(top=20)
    #% '\n'.join(['<li>%s</li>' % story.title for story in stories])
    return render(request, 'stories/index.html', {'stories':stories, 'user':request.user})

@login_required
def story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.moderator = request.user
            story.save()
            return HttpResponseRedirect('/')
    else:
        form = StoryForm()
    return render(request, 'stories/story.html', {'form': form})

@login_required
def vote(request):
    story = get_object_or_404(Story, pk = request.POST.get('story'))
    story.points +=1
    story.save()
    return HttpResponse()
        
