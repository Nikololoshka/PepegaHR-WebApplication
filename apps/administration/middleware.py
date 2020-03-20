from django.utils import timezone

from .models import HRUser


class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        """
        Обновляет время активности.
        """
        if request.user.is_authenticated:
            HRUser.objects.filter(id=request.user.id).update(last_visit=timezone.now())
