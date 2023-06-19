from django import forms
from user.models import Patient, Hospital, PatientProfile, HospitalProfile
from hospital.models import Doctor
from .models import Appointment, AppointmentReview,Medical


class AddPatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['first_name', 'last_name', 'address', 'pic', 'gender', 'phone', 'dob']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-field', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-field', 'placeholder': 'Last Name'}),
            'address': forms.TextInput(attrs={'class': 'form-field', 'placeholder': 'Address'}),
            'phone': forms.TextInput(attrs={'class':'form-field','type': 'tel'}),
            'dob': forms.DateInput(attrs={'class':'form-field','type': 'date'}),
            'gender': forms.Select(attrs={'class':'form-select-field'}),
        }

class AppointmentReviewForm(forms.ModelForm):
    class Meta:
        model = AppointmentReview
        fields = ['doctor_review', 'hospital_review']  

class AppointmentBookingForm(forms.ModelForm):
    appointment_date = forms.CharField(
        label='Date',
        widget=forms.DateInput(
            attrs={
                'class':'form-field',
                'type': 'date'
            })
    )
    appointment_time = forms.CharField(
        label='Time',
        widget=forms.DateInput(
            attrs={
                'class':'form-field',
                'type': 'time'
            })
    )

    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time']

class MedicalForm(forms.ModelForm):
    class Meta:
        model = Medical
        exclude = ['user']
        widgets = {
            'blood_type': forms.Select(attrs={'class': 'form-select-field'}),
            'allergies': forms.TextInput(attrs={'class': 'form-field'}),
            'chronic_conditions': forms.TextInput(attrs={'class': 'form-field'}),
            'medication': forms.TextInput(attrs={'class': 'form-field'}),
            
        }