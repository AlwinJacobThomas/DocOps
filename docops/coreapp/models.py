from django.db import models
from django.conf import settings
from user.models import Patient, Hospital
from hospital.models import Doctor
from django.core.validators import MinValueValidator

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments_as_patient')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='appointments_as_hospital')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    appointment_status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Appointment #{self.id}"

class AppointmentReview(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='appointment_review')
    doctor_rating = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    doctor_review = models.TextField(null=True, blank=True)
    hospital_rating = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    hospital_review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.id