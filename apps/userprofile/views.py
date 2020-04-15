from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods, require_GET

from .forms import ProfileEditForm


@login_required
@require_http_methods(['GET', 'POST'])
def my_profile_page(request: WSGIRequest):
    """
    Отображает профиль текущего пользователя.
    GET: Показывает страницу профиля текущего пользователя. 
    POST: Изменяет данные пользователя в профиле.
    """
    HRUser = get_user_model()

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=HRUser.objects.get(id=request.user.id))
        if form.is_valid():
            hr_user = form.save()
            update_session_auth_hash(request, hr_user)

            return redirect('my-profile')
    else:
        form = ProfileEditForm(instance=HRUser.objects.get(id=request.user.id))

    return render(request, 'userprofile/myprofile.html', {
        'profile_form': form
    })


@login_required
@require_GET
def profile_page(request: WSGIRequest, user_id: int):
    """
    Отображает страницу "чужого" профиля.
    """
    if request.user.id == user_id:
        return redirect('my-profile')

    HRUser = get_user_model()
    return render(request, 'userprofile/profile.html', {
        'hr_user': HRUser.objects.get(id=user_id)
    })