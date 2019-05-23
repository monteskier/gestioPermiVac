from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Treballadors

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Treballadors
        fields = ('username','first_name','last_name','dni','email','area','date_joined')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Treballadors
        fields = ('username','first_name','last_name','dni','email','area','date_joined')
