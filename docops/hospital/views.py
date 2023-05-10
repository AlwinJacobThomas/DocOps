from django.shortcuts import render,reverse,redirect
from .forms import AddHospitalProfileForm
from user.models import HospitalProfile
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

User = get_user_model()

def hospital(request):
    if request.user.is_authenticated:
        if request.user.role == 'HOSPITAL':
            try:
                hospital = request.user.hospital
                return render(request, 'hospital/hospital.html')
            except ObjectDoesNotExist:
                return redirect(reverse('hospital:add_profile'))
        elif request.user.role=='PATIENT':
            return redirect(reverse('coreapp:home'))
        else:
            return redirect('/admin/')
            
    else:    
        return render(request, 'hospital/landing.html')
    
@login_required
def AddProfile(request):
    if request.user.role == 'HOSPITAL':
        try:
            instance = request.user.hospital
            return redirect('hospital:edit_profile')
        except ObjectDoesNotExist:
            form = AddHospitalProfileForm()
            if request.method == "POST":
                form = AddHospitalProfileForm(request.POST, request.FILES)
                if form.is_valid():
                    post=form.save(commit=False)
                    post.location = request.POST['location']
                    post.user = User.objects.get(id=request.user.id)
                    if 'pic' in request.FILES:
                        post.pic = request.FILES['pic']
                    post.save()
                    return redirect(reverse('hospital:hospital'))
                else:
                    return render(request, 'hospital/add-profile.html', {
                        'form': form,
                        'error': True,
                    })
            return render(request,'hospital/add-profile.html',{
                'form': form,
                'error': False
            })
    else:
        return redirect('coreapp:home')

def EditProfile(request):
    if request.user.is_authenticated and request.user.role == 'HOSPITAL':
        try:
            instance = request.user.hospital
            form = AddHospitalProfileForm(instance=instance)
            if request.method == "POST":
                form = AddHospitalProfileForm(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    form.save()
                    return redirect(reverse('hospital:hospital'))
                else:
                    return render(request, 'hospital/add-profile.html', {
                        'form': form,
                        'error': True,
                    })
            
            return render(request,'hospital/add-profile.html',{
                'form': form,
                'error': False,
            })
        except ObjectDoesNotExist:   
            return redirect('coreapp:home')   