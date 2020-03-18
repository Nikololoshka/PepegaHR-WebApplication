from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from .models import HRUser


@login_required
def users(request: WSGIRequest):
    """
    Отображает страцу с пользователями, которые зарегистрированы в системе.
    """
    hr_users = HRUser.objects.all()

    return render(request, 'administration/users.html', {
        'hr_users': hr_users
    })


@login_required
def create_user(request: WSGIRequest):
    """
    Создает пользователя в HR системе.
    """
    if request.method == 'POST':
        # получение формы
        first_name: str = request.POST['first_name']
        last_name: str = request.POST['last_name']
        email: str = request.POST['email']
        password: str = request.POST['password']
        role: str = request.POST['role']

        

        return redirect('admin-users-page')

    return HttpResponse('Method not allowed')
