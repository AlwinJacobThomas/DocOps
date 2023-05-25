from django.db import models
from django.conf import settings
from user.models import Patient
# Create your models here.

# class Patient(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) 
#     def __str__(self):
#         return self.user

    
# class Schedule(models.Model):
    
#     def __str__(self):
#         return self.title
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

# ----------token generator----------
class TokenCounter(models.Model):
    date = models.DateField(default=date.today)
    counter = models.IntegerField(default=0)

    def __str__(self):
        return f"TokenCounter - {self.date}"

@receiver(post_save, sender=TokenCounter)
def update_token_counter(sender, instance, created, **kwargs):
    if created:
        instance.counter = 1
    else:
        instance.counter += 1
    instance.save()    
    # --------token------------
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=255)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    token_number = models.CharField(max_length=10, editable=False)
    appointment_status = models.CharField(max_length=255,choices=STATUS_CHOICES)

    def __str__(self):
        return f"Appointment #{self.id} - {self.patient_name}"
    
    def save(self, *args, **kwargs):
        if not self.token_number:
            token_counter, created = TokenCounter.objects.get_or_create(date=date.today())
            self.token_number = str(token_counter.counter).zfill(3)
        super().save(*args, **kwargs)

    
    
# class Hospital(models.Model):
    
#     def __str__(self):
#         return self.title

# class Doctor(models.Model):
    
#     def __str__(self):
#         return self.title    