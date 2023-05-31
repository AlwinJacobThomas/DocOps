from django import forms
from user.models import Patient, Hospital, PatientProfile, HospitalProfile
from .models import Doctor


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
    # pic = forms.ImageField(
    #     label='Profile Pic',
    #     widget=forms.FileInput(
    #         attrs={
    #             'id': 'imageUpload',
    #             'accept': '.png, .jpg, .jpeg'
    #         })
    # )

    class Meta:
        model = HospitalProfile
        fields = ['hospital_name', 'address', 'pic', 'location', 'phone', 'website']

class DoctorForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-field'}))
    specialization = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-field'}))
    qualifications = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-field'}))
    experience = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-field'}))
    contact_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-field'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-field'}))
    
    is_available = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-field'}))

    class Meta:
        model = Doctor
        exclude = ['hospital']


      


