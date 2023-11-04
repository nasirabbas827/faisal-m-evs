from django import forms
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'phone_number']  # Include all the fields you want to edit

class PasswordChangeCustomForm(PasswordChangeForm):
    pass
