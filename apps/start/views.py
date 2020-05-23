from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest


@csrf_exempt
def start(request: WSGIRequest):
    """
    Стартовая страница в системе.
    """
    if request.user.is_authenticated:
        return redirect('home-page')

    return render(request, 'registration/base.html')

