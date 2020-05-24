from django import template

register = template.Library()

@register.simple_tag()
def get_project_name():
    """
    Возвращает название проекта.
    """
    return 'MiromiroHR'
