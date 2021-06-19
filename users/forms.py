from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя')
    username = forms.CharField(label='Имя пользователя')
    email = forms.EmailField(label='Адрес электронной почты')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'email')
