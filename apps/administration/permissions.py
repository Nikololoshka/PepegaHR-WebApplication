from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden


def required_roles(roles=[]):
    """
    Проверяет, подходит ли роль текущего пользователя для доступа к странице.
    """
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            
            raise PermissionDenied()
            
        return wrap

    return decorator


def required_admin(view_func):
    """
    Проверяет, подходит ли роль текущего пользователя для доступа к странице.
    """
    def wrap(request, *args, **kwargs):
        if request.user.is_admin():
            return view_func(request, *args, **kwargs)

        raise PermissionDenied()

    return wrap


def required_moderator(view_func):
    """
    Проверяет, подходит ли роль текущего пользователя для доступа к странице.
    """
    def wrap(request, *args, **kwargs):
        if request.user.is_moderator():
            return view_func(request, *args, **kwargs)
            
        raise PermissionDenied()

    return wrap


def required_user(view_func):
    """
    Проверяет, подходит ли роль текущего пользователя для доступа к странице.
    """
    def wrap(request, *args, **kwargs):
        if request.user.is_user():
            return view_func(request, *args, **kwargs)
            
        raise PermissionDenied()

    return wrap
