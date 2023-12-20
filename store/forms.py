from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Client, Review

class ClientCreationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ("username", "email")

class ClientAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Client
        fields = ("username", "password")

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]
        labels = {
            'rating': 'Оцінка',
            'text': '',
        }