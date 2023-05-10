from django.shortcuts import render,redirect,reverse
from .forms import AddPatientProfileForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from user.models import HospitalProfile
# Create your views here.
User = get_user_model()

def home(request):
    context = {"profile":None}
    if request.user.is_authenticated:
        
        context = {
            "user" : request.user,
        }
        if request.user.role=='HOSPITAL':
            return redirect(reverse('hospital:hospital'))
        else :
            return render(request, 'coreapp/u-dash.html',context)
        
    else:   
        return render(request, 'coreapp/landing.html')

@login_required
def AddProfile(request):
    if request.user.is_authenticated and request.user.role == 'PATIENT':
        try:
            instance = request.user.patient
            # print("hiiii "+request.user.patient)
            return redirect('coreapp:home')
        except ObjectDoesNotExist:
            form = AddPatientProfileForm()
            if request.method == "POST":
                form = AddPatientProfileForm(request.POST, request.FILES)
                if form.is_valid():
                    post=form.save(commit=False)
                    post.user = User.objects.get(id=request.user.id)
                    if 'pic' in request.FILES:
                        post.pic = request.FILES['pic']
                    post.save() 
                    
                    return redirect(reverse('coreapp:home'))
                else:
                    return render(request, 'coreapp/add-profile.html', {
                        'form': form,
                        'error': True,
                    })
            return render(request,'coreapp/add-profile.html',{
                'form': form,
                'error': False
            })
    else:
        return redirect('coreapp:home')
def EditProfile(request):
    if request.user.is_authenticated and request.user.role == 'PATIENT':
        try:
            instance = request.user.patient
            form = AddPatientProfileForm(instance=instance)
            if request.method == "POST":
                form = AddPatientProfileForm(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    form.save()
                    return redirect(reverse('coreapp:home'))
                else:
                    return render(request, 'coreapp/add-profile.html', {
                        'form': form,
                        'error': True,
                    })
            
            return render(request,'coreapp/add-profile.html',{
                'form': form,
                'error': False,
            })
        except ObjectDoesNotExist:   
            return redirect('coreapp:home')   
        
@login_required
def c_dash(request):
    return render(request, 'coreapp/c-dash.html')
@login_required
def p_dash(request):
    return render(request, 'coreapp/p-dash.html')

@login_required
def profile(request):
    if request.user.is_authenticated and request.user.role == 'PATIENT':
        context = {
            "user":request.user,
        }
    return render(request, 'coreapp/profile.html',context)
@login_required
def edit_profile(request):
    return render(request, 'coreapp/edit-profile.html')


@login_required
def appointment(request):
    return render(request, 'coreapp/appointment.html')

@login_required
def doc_search(request):

    return render(request, 'coreapp/doc-search.html')
@login_required
def hos_search(request):
    if request.user.is_authenticated and request.user.role == 'PATIENT':
        context = {
            "hospitals":HospitalProfile.objects.all()
        }
    return render(request, 'coreapp/hos-search.html',context)



