from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import *

# Create your views here.

@login_required
def dashboard(request):
    backlogs = ProductBacklog.objects.all()
    teams = Team.objects.all()
    return render(request, 'balengou/dashboard.html', { 'backlogs':backlogs, 'teams':teams })

@login_required
def backlog(request, backlog_id):
    backlog = get_object_or_404(ProductBacklog, pk=backlog_id)
    stories = UserStory.objects.filter(product_backlog=backlog)
    return render(request,'balengou/backlog.html', { 'backlog':backlog, 'stories': stories })
