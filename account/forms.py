from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm


class MyUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label="名字/暱稱",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')


class MyUserChangeForm(forms.ModelForm):
    first_name = forms.CharField(
        label="名字/暱稱",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    about = forms.CharField(
        label="個人簡介",
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False
    )
    class Meta:
        model = User
        fields = ('first_name', 'email', 'about')


class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='舊密碼',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label='新密碼',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label='新密碼確認',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class ChangeAvatarForm(forms.ModelForm):
    avatar = forms.ImageField()
    class Meta:
        model = User
        fields = ('avatar',)