from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class ProfileEditForm(forms.ModelForm):
    """
    Форма для редактирования пользователя.
    """
    password = forms.CharField(widget=forms.PasswordInput(), \
         label=_('Новый пароль'), required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), \
         label=_('Подтвердите новый пароль'), required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
        labels = {
            'username': _('Username'),
            'email': _('Email'),
        }
        help_texts = {
            'username': _('Латинские буквы, цифры и @ / . / + / - / _')
        }
        error_messages = {
            'username': {
                'unique': _('Пользователь с таким username уже существует')
            }
        }

    def clean(self):
        """
        Валидация всей формы, в целом.
        """
        cleaned_data = super(ProfileEditForm, self).clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError(_('Пароли не совпадают'))

    def save(self, commit=True):
        """
        Сохранение отредактированной формы в БД.
        """
        hr_user = super(ProfileEditForm, self).save(commit=False)
        
        password = self.cleaned_data['password']
        if password is not None and password:
            hr_user.set_password(password)

        if commit:
            hr_user.save()

        return hr_user
