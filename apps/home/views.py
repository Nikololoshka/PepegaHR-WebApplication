from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest


@login_required
def home(request: WSGIRequest):
    return render(request, 'home/base.html')
