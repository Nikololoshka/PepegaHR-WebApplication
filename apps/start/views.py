from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest


@csrf_exempt
def start(request: WSGIRequest):
    return render(request, 'registration/base.html')

