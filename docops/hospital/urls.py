from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns =[
    path('',views.hospital,name='hospital'),
    path('add_profile',views.AddProfile,name='add_profile'),
    path('edit_profile',views.EditProfile,name='edit_profile'),
]