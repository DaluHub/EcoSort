from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, WastePickupRequest, UpgradeRequest

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

class UpgradeRequestForm(forms.ModelForm):
    class Meta:
        model = UpgradeRequest
        exclude = ['user', 'approved', 'declined', 'created_at']
        widgets = {
            'justification': forms.Textarea(attrs={'rows': 3}),
            'service_areas': forms.Textarea(attrs={'rows': 2}),
            'certifications': forms.Textarea(attrs={'rows': 2}),
            'sustainability_practices': forms.Textarea(attrs={'rows': 2}),
        }
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('terms_agreed') or not cleaned_data.get('privacy_agreed'):
            raise forms.ValidationError("You must agree to the terms and privacy policy.")

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