from django.db import models
from django.forms import ModelForm
from .models import Bd, Comment, Images
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import user_registrated
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from snowpenguin.django.recaptcha2.widgets import Widget



class BdForm(ModelForm):
    class Meta:
        model = Bd
        fields = ('title', 'content', 'price', 'rubric')


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Images
        fields = ('image', )


class AuthUserForm(AuthenticationForm, ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget(explicit=True), label='Докажи что не робот')
    class Meta:
        model=User
        fields=('username', 'password')

class RegisterUserForm(ModelForm):
    username=forms.CharField(label='Имя пользователя')
    class Meta:
        model=User
        fields=('username', 'email', 'password')

    def save(self, commit=True):
        ''' :return: delay user activation until mail confirmation
        '''
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label='Текущий пароль')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Новый пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль')


