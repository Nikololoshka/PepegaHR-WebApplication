from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings


from .models import HRUser, Departament


class HRUserBasicForm(forms.ModelForm):
    """
    Форма для редактирования пользователя.
    """
    class Meta:
        model = HRUser
        fields = ['photo', 'first_name', 'last_name', 'username', 'email', 'role']
        labels = {
            'photo': _('Фото профиля'),
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'username': _('Username'),
            'email': _('Email'),
            'role': _('Роль')
        }
        help_texts = {
            'username': _('Латинские буквы, цифры и @ / . / + / - / _')
        }
        error_messages = {
            'username': {
                'unique': _('Пользователь с таким username уже существует')
            }
        }


class HRUserCreateForm(HRUserBasicForm):
    """
    Форма создания пользователя. 
    """
    password = forms.CharField(widget=forms.PasswordInput(), \
         label=_('Пароль'), required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), \
         label=_('Подтвердите пароль'), required=True)

    def clean(self):
        """
        Валидация всей формы, в целом.
        """
        cleaned_data = super(HRUserCreateForm, self).clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError(_('Пароли не совпадают'))

    def save(self, commit=True):
        """
        Сохранение созданой формы в БД.
        """
        hr_user = super(HRUserCreateForm, self).save(commit=False)
        
        password = self.cleaned_data['password']
        hr_user.set_password(password)

        if commit:
            hr_user.save()

        return hr_user


class HRUserEditForm(HRUserBasicForm):
    """
    Форма редактирования формы.
    """
    password = forms.CharField(widget=forms.PasswordInput(), \
         label=_('Новый пароль'), required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), \
         label=_('Подтвердите новый пароль'), required=False)

    def clean(self):
        """
        Валидация всей формы, в целом.
        """
        cleaned_data = super(HRUserEditForm, self).clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError(_('Пароли не совпадают'))

    def save(self, commit=True):
        """
        Сохранение отредактированной формы в БД.
        """
        hr_user = super(HRUserEditForm, self).save(commit=False)
        
        password = self.cleaned_data['password']
        if password is not None and password:
            hr_user.set_password(password)

            if settings.DEBUG:
                print(f'Change password for {hr_user.id} to: {password}')

        if commit:
            hr_user.save()

        return hr_user


class DepartamentForm(forms.ModelForm):
    """
    Форма по созданию группы.
    """
    class Meta:
        model = Departament
        fields = ['name']
        labels = {
            'name': _('Название группы')
        }
