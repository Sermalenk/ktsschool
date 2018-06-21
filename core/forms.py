from django import forms
from django.contrib.auth.forms import UsernameField, AuthenticationForm

from core.models import Message


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PrettyLoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text',]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        message = super().save(commit=False)
        message.author = self.user
        if commit:
            message.save()
        return message
