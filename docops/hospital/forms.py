from django import forms
from user.models import HospitalProfile
from .models import Doctor,Facility
import re

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
   

    class Meta:
        model = HospitalProfile
        fields = ['hospital_name', 'address', 'pic', 'location', 'phone', 'website']

class DoctorForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-field'}))
    specialization = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-field'}))
    qualifications = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-field'}))
    experience = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-field'}))
    contact_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-field','type':'phone'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-field','type':'email'}))
    
    is_available = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-field'}))

    class Meta:
        model = Doctor
        exclude = ['hospital']

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ('name', 'description', 'opening_time', 'closing_time', 'is_available')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-field'}),
            'description': forms.Textarea(attrs={'class': 'form-field'}),
            'opening_time': forms.TimeInput(attrs={'class': 'form-field', 'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'class': 'form-field', 'type': 'time'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-field'}),
        }
      


