from django.shortcuts import render,redirect,reverse
from user.models import HospitalProfile, PatientProfile
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    context = {"profile":None}
    if request.user.is_authenticated:
        
        context = {
            "user" : request.user,
        }
        if request.user.role=='HOSPITAL':
            return redirect('coreapp:hospital')
        else :
            return render(request, 'patient/u-dash.html',context)
        
    else:   
        return render(request, 'patient/landing.html')
    
@login_required
def c_dash(request):
    return render(request, 'patient/c-dash.html')
@login_required
def p_dash(request):
    return render(request, 'patient/p-dash.html')

@login_required
def profile(request):
    return render(request, 'patient/profile.html')
@login_required
def edit_profile(request):
    return render(request, 'patient/edit-profile.html')


@login_required
def appointment(request):
    return render(request, 'patient/appointment.html')

@login_required
def doc_search(request):
    return render(request, 'patient/doc-search.html')
@login_required
def hos_search(request):
    return render(request, 'patient/hos-search.html')



def hospital(request):
    context = {"profile":None}
    if request.user.is_authenticated:
        
        context = {
            "user" : request.user,
        }
        if request.user.role=='HOSPITAL':
            return render(request, 'hospital/hospital.html', context)
        elif request.user.role=='PATIENT':
            return redirect(reverse('coreapp:home'))
        else:
            return redirect('admin')
    else:    
        return render(request, 'hospital/Landing.html')