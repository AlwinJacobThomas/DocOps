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
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('appointment',views.appointment,name='appointment'),



    path('hospital/',views.hospital,name='hospital'),
    
]