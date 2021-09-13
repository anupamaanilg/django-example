from django import forms
from django.contrib.auth.models import User
from login_app.models import UserProfileInfo

class UserProfileInfoForm(forms.ModelForm):
    portfolio = forms.URLField(required=False)
    picture = forms.ImageField(required=False)
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio', 'picture')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'email','password')
