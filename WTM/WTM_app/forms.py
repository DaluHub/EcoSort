from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, WastePickupRequest

class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        "password_mismatch": "The two password fields didn’t match. Please try again.",
    }

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class WastePickupRequestForm(forms.ModelForm):
    class Meta:
        model = WastePickupRequest
        fields = ['company', 'address', 'scheduled_date']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].empty_label = "Select a company"