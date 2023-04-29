from django import forms
from user.models import Patient, Hospital, PatientProfile, HospitalProfile


class AddPatientProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label='first Name',
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': 'First Name'
            })
    )
    last_name = forms.CharField(
        label='last Name',
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': 'Last Name'
            })
    )
    address = forms.CharField(
        label='Address',
        widget=forms.TextInput(
            attrs={
                'class': 'address',
                'placeholder': 'Address'
            })
    )
    pic = forms.ImageField(
        label='Profile Pic',
        widget=forms.FileInput(
            attrs={
                'id': 'imageUpload',
                'accept': '.png, .jpg, .jpeg'
            })
    )

    class Meta:
        model = PatientProfile
        fields = ['first_name','last_name', 'address', 'pic', ]
