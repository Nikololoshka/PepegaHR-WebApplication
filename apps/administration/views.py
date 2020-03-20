from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest

from .models import HRUser


@login_required
def users_page(request: WSGIRequest):
    """
    Отображает страцу с пользователями, которые зарегистрированы в системе.
    """
    hr_users = HRUser.objects.all()

    return render(request, 'administration/users.html', {
        'hr_users': hr_users
    })


@login_required
def create_user_page(request: WSGIRequest):
    """
    Отображает страницу для создания пользователя в HR системе.
    """
    return render(request, 'administration/create_user.html')


@login_required
def create_user(request: WSGIRequest):
    if request.method == 'POST':
        # получение формы
        first_name: str = request.POST['first_name']
        last_name: str = request.POST['last_name']
        nickname: str = request.POST['nickname']
        email: str = request.POST['email']
        password: str = request.POST['password']
        role: str = request.POST['role']

        hr_user = HRUser(first_name=first_name,
                         last_name=last_name,
                         username=nickname,
                         email=email,
                         password=password,
                         role=role)
        hr_user.save()
        return redirect('admin-users-page')

    return HttpResponse('Method not allowed')
