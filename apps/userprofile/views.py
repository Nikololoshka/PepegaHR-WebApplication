from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model


@login_required
def profile_page(request: WSGIRequest):
    """
    Показывает страницу профиля текущего пользователя. 
    """
    return render(request, 'userprofile/profile.html')

@login_required
def profile_edit(request: WSGIRequest):
    """
    Изменяет данные пользователя в профиле.
    """
    if request.method == 'POST':
        nickname: str = request.POST.get('nickname', None)
        email: str = request.POST.get('email', None)
        password: str = request.POST.get('password', None)

        HRUser = get_user_model()
        hr_user = HRUser.objects.get(id=request.user.id)
        hr_user.username = nickname
        hr_user.email = email

        if password is not None and len(password) >= 8:
            hr_user.set_password(password)

        hr_user.save()
        update_session_auth_hash(request, hr_user)

        return redirect('profile-page')

    return HttpResponse('Method not allowed')
