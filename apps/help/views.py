from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest


def quick_start_page(request: WSGIRequest):
    return render(request, 'help/quick_start.html')
