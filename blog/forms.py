from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]
        
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"}),
        }
    

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = get_user_model().objects.filter(username=username)
        if self.instance:  # editing existing user
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = get_user_model().objects.filter(email=email)
        if self.instance:  # editing existing user
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already registered.")
        return email

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"})
    )