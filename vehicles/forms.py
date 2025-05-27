from django import forms
from .models import Message, VehicleImage, Vehicle
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your message...'}),
        }

# 👇 Bu doğru yapı
VehicleImageFormSet = inlineformset_factory(
    Vehicle,
    VehicleImage,
    fields=('image',),
    extra=3,
    can_delete=True
)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
