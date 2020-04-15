from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from .models import HRUser, Departament
from .forms import HRUserCreateForm, HRUserEditForm

@login_required
@require_GET
def users_page(request: WSGIRequest):
    """
    Отображает страцу с пользователями, которые зарегистрированы в системе.
    """
    hr_users = HRUser.objects.all()

    page_num = request.GET.get('page', 1)

    paginator = Paginator(hr_users, 30)
    page = paginator.get_page(page_num)

    return render(request, 'administration/users/users.html', {
        'hr_users': hr_users,
        'page': page
    })


@login_required
@require_http_methods(['GET', 'POST'])
def create_user_page(request: WSGIRequest):
    """
    Осуществляет взамодействие с созданием пользователя.

    GET: Отображает страницу для создания пользователя в HR системе.
    POST: Создает пользователя в системе.
    """
    if request.method == 'POST':
        # получение формы
        form = HRUserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-users-page')

    else:
        form = HRUserCreateForm()

    return render(request, 'administration/users/create_user.html', {
            'hr_form': form
        })
    

@login_required
@require_http_methods(['GET', 'POST'])
def edit_user_page(request: WSGIRequest, user_id: int):
    """
    Осуществляет взамодействие с созданием пользователя.

    GET: Отображает страницу для редактирования пользователя в HR системе.
    POST: Редактирует пользователя в системе.
    """
    if request.method == 'POST':
        # получение формы
        form = HRUserEditForm(request.POST, request.FILES, instance=HRUser.objects.get(id=user_id))

        if form.is_valid():
            form.save()
            return redirect('admin-users-page')

        # TODO: изменение фото пользователя
        # без изменений: None, old_photo
        # к default: None, ""
        # с изменениями new_photo, old_photo

        # if photo is not None:
        #     # есть новая
        #     hr_user.photo = photo

        # elif photo_old is None or not photo_old:
        #     # нет старого, т.е. default состоянию
        #     hr_user.photo.delete()

    else:
        hr_user = HRUser.objects.get(id=user_id)
        form = HRUserEditForm(instance=hr_user)
    
    return render(request, 'administration/users/edit_user.html', {
            'hr_form': form
        })

@login_required
@require_POST
def remove_user(request: WSGIRequest):
    """
    Удаляет пользователя из системы.
    """
    user_id = request.POST['id']
    hr_user = HRUser.objects.get(pk=user_id)
    if hr_user is not None:
        hr_user.delete()
        return redirect('admin-users-page')

    return HttpResponse('Cannot remove user')


@login_required
@require_GET
def departaments_page(request: WSGIRequest):
    departaments = Departament.objects.all()

    page_num = request.GET.get('page', 1)

    paginator = Paginator(departaments, 30)
    page = paginator.get_page(page_num)

    return render(request, 'administration/departaments/departaments.html', {
        'departaments': departaments,
        'page': page
    })


@login_required
@require_GET
def information_page(request: WSGIRequest):
    return render(request, 'administration/information.html')
    