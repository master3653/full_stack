from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):    #登录
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(label='密码',widget=forms.PasswordInput)
    password2=forms.CharField(label='再次输入密码',widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('username','first_name','email')
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('二次密码不匹配')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username','first_name','email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('date_of_birth','photo')