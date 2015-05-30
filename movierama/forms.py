__author__ = 'evangelie'
from django.contrib.auth.models import User
from django import forms
from movierama.models import Movies



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class MovieForm(forms.ModelForm):

    class Meta:
        model = Movies
        exclude = ('date', 'likes', 'hates','status',)




