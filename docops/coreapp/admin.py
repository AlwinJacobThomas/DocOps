from django.contrib import admin
from .models import Appointment, AppointmentReview
# Register your models here.


admin.site.register(Appointment)
admin.site.register(AppointmentReview)