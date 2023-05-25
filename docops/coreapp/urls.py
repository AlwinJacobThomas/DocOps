from django.urls import path
from . import views

app_name = 'coreapp'

urlpatterns =[
    path('',views.home,name='home'),
    path('p_dash',views.p_dash,name='p_dash'),
    path('c_dash',views.c_dash,name='c_dash'),
    path('doc_search',views.doc_search,name='doc_search'),
    path('hos_search',views.hos_search,name='hos_search'),
    path('profile',views.profile,name='profile'),
    #changed the edit profile view
    path('edit_profile',views.EditProfile,name='edit_profile'),
    path('add_profile',views.AddProfile,name='add_profile'),
    path('appointment',views.appointment,name='appointment'),

    #doctor
    path('booking',views.booking,name='booking'),
    path('doctor_profile/<int:doctor_id>',views.DoctorProfile,name='doctor_profile'),
    path('doctor/<int:doctor_id>/review/', views.AddReview, name='add_review'),
    path('doctor_booking/<int:doctor_id>',views.doctor_booking,name='doctor_booking'),
]