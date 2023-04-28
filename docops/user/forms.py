from django import forms
from .models import Patient,Hospital,PatientProfile
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model



class SignupForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'input',
                'placeholder': 'user@example.com'
            })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'password',
                'placeholder': 'password'
            })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "password",
                "placeholder": "confirm password"
            })
    )

    class Meta:
        model = Patient
        fields = ['email', 'password1', 'password2',]


class LoginForm(AuthenticationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'input',
                'placeholder': 'user@example.com'
            })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'password',
                'placeholder': 'password'
            })
    )

    class Meta:
        model = Patient
        fields = "__all__"

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First Name',
        widget=forms.PasswordInput(
            attrs={
                'class': 'text',
                'placeholder': 'First Name'
            })        

    )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.PasswordInput(
            attrs={
                'class': 'text',
                'placeholder': 'Last Name'
            })        

    )
    address = forms.CharField(
        label='Address',
        widget=forms.TextInput(
            attrs={
                'class': 'textarea',
                'placeholder': 'Address'
            })        

    )
    pic = forms.ImageField(
        label='Profile Picture',
        widget=forms.TextInput(
            attrs={
                'class': 'pic_upload'
            })        

    )      

    class Meta:
        model = PatientProfile
        fields = "__all__"

class HosSignupForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'input',
                'placeholder': 'user@example.com'
            })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'password',
                'placeholder': 'password'
            })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'password2',
                'placeholder': 'Confirm password'
            })

    )

    class Meta:
        model = Hospital
        fields = ['email', 'password1', 'password2',]


class HosLoginForm(AuthenticationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'input',
                'placeholder': 'user@example.com'
            })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'password',
                'placeholder': 'password'
            })
    )

    class Meta:
        model = Hospital
        fields = "__all__"
