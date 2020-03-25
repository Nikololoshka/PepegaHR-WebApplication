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
    """
    Создает пользователя в системе.
    """
    if request.method == 'POST':
        # получение формы
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        nickname = request.POST['nickname']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        photo = request.FILES.get('profile_image', None)

        params = {
            'first_name': first_name,
            'last_name': last_name,
            'username': nickname,
            'email': email,
            'role': role,
        }

        if photo is not None:
            params['photo'] = photo

        hr_user = HRUser(**params)
        hr_user.set_password(password)
        hr_user.save()

        return redirect('admin-users-page')

    return HttpResponse('Method not allowed')


@login_required
def remove_user(request: WSGIRequest):
    """
    Удаляет пользователя из системы.
    """
    if request.method == 'POST':
        user_id = request.POST['id']
        hr_user = HRUser.objects.get(pk=user_id)
        if hr_user is not None:
            hr_user.delete()
            return redirect('admin-users-page')

        return HttpResponse('Cannot remove user')

    return HttpResponse('Method not allowed')
