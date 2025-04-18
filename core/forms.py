from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from .models import UserProfile


class ProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "e.g. +44 7700 900 123"})
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Your address"})
    )

    class Meta:
        model = UserProfile
        fields = ["phone_number", "address"]

    def clean_phone_number(self):
        value = self.cleaned_data["phone_number"]
        if value and not re.fullmatch(r"\+?\d[\d\-\s]{7,}$", value):
            raise forms.ValidationError("Enter a valid phone number.")
        return value


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address']
