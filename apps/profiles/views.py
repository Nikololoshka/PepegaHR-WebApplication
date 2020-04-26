from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods, require_GET

# from apps.administration.permissions import required_admin

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

    return render(request, 'profiles/myprofile.html', {
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
    return render(request, 'profiles/profile.html', {
        'hr_user': HRUser.objects.get(id=user_id)
    })


@login_required
@require_GET
def departament_page(request: WSGIRequest, departament_id: int):
    """
    Отображает страницу с группой.
    """
    HRUser = get_user_model()
    Departament = HRUser.get_departament_model()

    departament = Departament.objects.get(id=departament_id)
    users = departament.hruser_set.all()

    # пагинация
    page_num = request.GET.get('page', 1)
    paginator = Paginator(users, 30)
    page = paginator.get_page(page_num)

    return render(request, 'profiles/departament.html', {
        'departament': departament,
        'page': page
    })


