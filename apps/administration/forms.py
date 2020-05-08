from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings


from .models import HRUser, Departament


class HRUserForm(forms.ModelForm):
    """
    Форма создания (редактирования) пользователя. 
    """
    password = forms.CharField(widget=forms.PasswordInput(), \
         label=_('Пароль'), required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), \
         label=_('Подтвердите пароль'), required=True)

    class Meta:
        model = HRUser
        fields = ['photo', 'first_name', 'last_name', 'username', 'email', 'role', 'departaments']
        labels = {
            'photo': _('Фото профиля'),
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'username': _('Username'),
            'email': _('Email'),
            'role': _('Роль'),
            'departaments': _('Группы')
        }
        help_texts = {
            'username': _('Латинские буквы, цифры и @ / . / + / - / _')
        }
        error_messages = {
            'username': {
                'unique': _('Пользователь с таким username уже существует')
            }
        }

    def __init__(self, *args, **kwargs):
        super(HRUserForm, self).__init__(*args, **kwargs)
        
        # если редактируем
        if self.instance.id is not None:
            self.fields['password'].label = _('Новый пароль')
            self.fields['password'].required = False
            self.fields['password_confirm'].label = _('Подтвердите новый пароль')
            self.fields['password_confirm'].required = False

    def clean(self):
        """
        Валидация всей формы, в целом.
        """
        cleaned_data = super(HRUserForm, self).clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError(_('Пароли не совпадают'))

    def save(self, commit=True):
        """
        Сохранение созданой формы в БД.
        """
        hr_user = super(HRUserForm, self).save(commit=False)
        
        if hasattr(hr_user, 'password'):
            if password is not None and password:
                hr_user.set_password(password)
        else:
            password = self.cleaned_data['password']
            hr_user.set_password(password)

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
