from django import forms
# from django.contrib.auth.models import User
from users.models import User

class RegisterForm(forms.Form):
    """Registration form"""
    username = forms.CharField(required=True, min_length=4, max_length=50, 
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': 'Username'
        }
    ))

    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': 'youremail@mail.com'
        }
    ))

    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'password',
        }
    ))

    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'password',
        }
    ))

    def clean_username(self):
        """Validates if user exists"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario ya existe')
        return username

    def clean_email(self):
        """Validates if email is not in use"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya está en uso')      
        return email
    
    def save(self):
        """Saves the info"""
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )
