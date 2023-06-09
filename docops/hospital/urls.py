from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns =[
    path('',views.hospital,name='hospital'),
    path('add_profile',views.AddProfile,name='add_profile'),
    path('edit_profile',views.EditProfile,name='edit_profile'),
    path('doctor_profile/<int:doctor_id>',views.DoctorProfile,name='doctor_profile'),
    
    path('add_doctor',views.AddDoctor,name='add_doctor'),
    path('edit_doctor/<int:doctor_id>',views.EditDoctor,name='edit_doctor'),
    path('delete_doctor/<int:doctor_id>',views.DeleteDoctor,name='delete_doctor'),
    
    path('doctor_list',views.DoctorList,name='doctor_list'),
]