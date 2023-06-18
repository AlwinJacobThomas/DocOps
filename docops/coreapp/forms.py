from django import forms
from user.models import Patient, Hospital, PatientProfile, HospitalProfile
from hospital.models import Doctor
from .models import Appointment, AppointmentReview,Medical

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
    # pic = forms.ImageField(
    #     label='Profile Pic',
    #     widget=forms.FileInput(
    #         attrs={
    #             'id': 'imageUpload',
    #             'accept': '.png, .jpg, .jpeg'
    #         })
    # )

    class Meta:
        model = PatientProfile
        fields = ['first_name','last_name', 'address', 'pic', 'gender', 'phone', 'dob']



class AppointmentReviewForm(forms.ModelForm):
    class Meta:
        model = AppointmentReview
        fields = ['doctor_review', 'hospital_review']  

class AppointmentBookingForm(forms.ModelForm):
    appointment_date = forms.CharField(
        label='Date',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'oninput': "this.className = ''"
            })
    )
    appointment_time = forms.CharField(
        label='Time',
        widget=forms.DateInput(
            attrs={
                'type': 'time',
                'oninput': "this.className = ''"
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