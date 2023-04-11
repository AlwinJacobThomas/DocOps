from django import forms
from user.models import Patient, Hospital, PatientProfile, HospitalProfile


class AddHospitalProfileForm(forms.ModelForm):
    hospital_name = forms.CharField(
        label='Hospital Name',
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': 'Hospital Name'
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
        model = HospitalProfile
        fields = ['hospital_name', 'address', 'pic', ]
