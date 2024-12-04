from django import forms
from .models import FoodEntry
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ['food_item', 'calories', 'date', 'notes']

class EmailVerificationForm(forms.Form):
    verification_code = forms.CharField(max_length=4, required=True)

class PasswordResetForm(forms.Form):
    verification_code = forms.CharField(max_length=4, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)

class ResetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
