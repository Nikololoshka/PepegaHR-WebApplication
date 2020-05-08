from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.utils.translation import gettext_lazy as _

from .models import HRUser, Departament
from .forms import HRUserForm, DepartamentForm
from .permissions import required_admin


@login_required
@required_admin
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
        'page': page
    })


@login_required
@required_admin
@require_http_methods(['GET', 'POST'])
def hr_user_page(request: WSGIRequest, user_id: int = None):
    """
    Осуществляет взамодействие с созданием (редактированием) пользователя.

    GET: Отображает страницу для создания (редактирования) пользователя в HR системе.
    POST: Создает (редактирует) пользователя в системе.
    """
    instance = get_object_or_404(HRUser, id=user_id) if user_id is not None else None

    if request.method == 'POST':
        # получение формы
        form = HRUserForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form.save()
            form.save_m2m()

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
            
            return redirect('admin-users-page')

    else:
        form = HRUserForm(instance=instance)

    return render(request, 'administration/users/hr_user.html', {
            'hr_form': form,
            'user_id': user_id,
            'action': _('Добавить') if instance is None else _('Изменить'),
            'title_action': _('Создание') if instance is None else _('Редактирование')
        })
    

@login_required
@required_admin
@require_POST
def remove_user(request: WSGIRequest):
    """
    Удаляет пользователя из системы.
    """
    user_id = request.POST['id']
    hr_user = get_object_or_404(HRUser, id=user_id)

    hr_user.delete()
    return redirect('admin-users-page')


@login_required
@required_admin
@require_http_methods(['GET', 'POST'])
def departaments_page(request: WSGIRequest):
    """
    GET: Отображает страницу с группами.
    POST: Создает новую группу для пользователей.
    """
    if request.method == 'POST':
        # получение формы
        form = DepartamentForm(request.POST)
        if form.is_valid():
            form.save()
            form = DepartamentForm()

    else:
        form = DepartamentForm()

    departaments = Departament.objects.all()

    page_num = request.GET.get('page', 1)
    paginator = Paginator(departaments, 30)
    page = paginator.get_page(page_num)

    return render(request, 'administration/departaments/departaments.html', {
        'departament_form': form,
        'page': page
    })


@login_required
@required_admin
@require_http_methods(['GET', 'POST'])
def departament_page(request: WSGIRequest, departament_id: int):
    """
    GET: Отображает страницу текущей группы.
    POST: Изменяет данные текущей группы.
    """
    departament = get_object_or_404(Departament, id=departament_id)
    users = departament.hruser_set.all()

    if request.method == 'POST':
        form = DepartamentForm(request.POST, instance=departament)
        if form.is_valid():
            departament = form.save()

            form = DepartamentForm(instance=departament)
        
    else:
        form = DepartamentForm(instance=departament)

    # пагинация
    page_num = request.GET.get('page', 1)
    paginator = Paginator(users, 30)
    page = paginator.get_page(page_num)

    return render(request, 'administration/departaments/departament.html', {
        'departament': departament,
        'departament_form': form,
        'page': page
    })


@login_required
@required_admin
@require_POST
def departament_remove(request: WSGIRequest, departament_id: int):
    """
    Удаляет группу, но не пользователей (лишь из группы, соответсвенно).
    """
    departament = get_object_or_404(Departament, id=departament_id)
    departament.hruser_set.clear()
    departament.delete()
    
    return redirect('admin-departaments-page')


@login_required
@required_admin
@require_POST
def departament_remove_user(request: WSGIRequest, departament_id: int):
    """
    Удаляет пользователя из группы.
    """
    user_id: int = request.POST.get('user_id', None)
    if user_id is not None:
        hr_user = get_object_or_404(HRUser, id=user_id)
        departament = get_object_or_404(Departament, id=departament_id)

        hr_user.departaments.remove(departament)

    return redirect('admin-departament-page', departament_id=departament_id)


@login_required
@required_admin
@require_GET
def information_page(request: WSGIRequest):
    """
    Отображает страницу с информацией по администрированию.
    """
    hr_users = HRUser.objects.all()
    departaments = Departament.objects.all()
    last_users = hr_users.filter(last_visit__isnull=False).order_by('-last_visit')[:5]

    return render(request, 'administration/information.html', {
        'hr_users_count': hr_users.count(),
        'departaments_count': departaments.count(),
        'last_users': last_users
    })
    