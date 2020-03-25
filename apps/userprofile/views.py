from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest


@login_required
def profile_page(request: WSGIRequest):
    return render(request, 'userprofile/profile.html')

@login_required
def profile_edit(request: WSGIRequest):
    pass
