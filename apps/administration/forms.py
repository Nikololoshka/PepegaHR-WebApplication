from django import forms
from .models import HRUser


class HRUserForm(forms.ModelForm):
    """
    Форма для редактирования пользователе.
    """
    password = forms.CharField(widget=forms.PasswordInput(), \
         label='Пароль', required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), \
         label='Подтвердите пароль', required=False)

    class Meta:
        model = HRUser
        fields = ['photo', 'first_name', 'last_name', 'username', 'email', 'role']
        labels = {
            'photo': 'Фото профиля',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Username',
            'email': 'Email',
            'role': 'Роль'
        }
        help_texts = {
            'username': 'Латинские буквы, цифры и @ / . / + / - / _'
        }
        error_messages = {
            'username': {
                'unique': 'Пользователь с таким username уже существует'
            }
        }

    def clean(self):
        cleaned_data = super(HRUserForm, self).clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')

    def save(self, commit=True):
        hr_user = super(HRUserForm, self).save(commit=False)
        
        password = self.cleaned_data['password']
        if password is not None and password:
            hr_user.set_password(self.cleaned_data['password'])
            print('Chage password to: ' + password)
            if commit:
                hr_user.save()

        return hr_user
