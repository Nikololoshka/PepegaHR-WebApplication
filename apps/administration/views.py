from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from .models import HRUser
from .forms import HRUserForm

@login_required
def users_page(request: WSGIRequest):
    """
    Отображает страцу с пользователями, которые зарегистрированы в системе.
    """
    hr_users = HRUser.objects.all()

    page_num = request.GET.get('page', 1)

    paginator = Paginator(hr_users, 30)
    page = paginator.get_page(page_num)

    return render(request, 'administration/users.html', {
        'hr_users': hr_users,
        'page': page
    })


@login_required
def create_user_page(request: WSGIRequest):
    """
    Отображает страницу для создания пользователя в HR системе.
    """
    return render(request, 'administration/create_user.html')


@login_required
def create_user_model(request: WSGIRequest):
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
def edit_user_page(request: WSGIRequest, user_id: int):
    """
    Отображает страницу для редактирования пользователя в HR системе.
    """
    hr_user = HRUser.objects.get(id=user_id)
    return render(request, 'administration/edit_user.html', {
        'hr_user': hr_user,
        'roles': HRUser.USER_ROLES,
        'hr_form': HRUserForm(instance=hr_user)
    })


@login_required
@require_POST
def edit_user_model(request: WSGIRequest, user_id: int):
    # получение формы
    # first_name = request.POST.get('first_name', None)
    # last_name = request.POST.get('last_name', None)
    # nickname = request.POST.get('nickname', None)
    # email = request.POST.get('email', None)
    # password = request.POST.get('password', None)
    # role = request.POST.get('role', None)
    # photo_old = request.POST.get('profile_image_old', None)
    # photo = request.FILES.get('profile_image', None)

    form = HRUserForm(request.POST, request.FILES, instance=HRUser.objects.get(id=user_id))
    print(form.is_valid())
    print(form.changed_data)
    print(form.errors)

    if form.is_valid():
        form.save()
        return redirect('admin-users-page')

    return render(request, 'administration/edit_user.html', {
        'hr_form': form
        })

    # без изменений: None, old_photo
    # к default: None, ""
    # с изменениями new_photo, old_photo

    # if photo is not None:
    #     # есть новая
    #     hr_user.photo = photo

    # elif photo_old is None or not photo_old:
    #     # нет старого, т.е. default состоянию
    #     hr_user.photo.delete()


@login_required
def remove_user_model(request: WSGIRequest):
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
