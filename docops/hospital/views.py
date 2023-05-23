from django.shortcuts import render, reverse, redirect
from .forms import AddHospitalProfileForm
from user.models import HospitalProfile
from .models import Doctor, DoctorReview
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import DoctorForm
from django.http import Http404

User = get_user_model()


def hospital(request):
    if request.user.is_authenticated:
        if request.user.role == 'HOSPITAL':
            try:
                hospital = request.user.hospital
                return render(request, 'hospital/hospital.html')
            except ObjectDoesNotExist:
                return redirect(reverse('hospital:add_profile'))
        elif request.user.role == 'PATIENT':
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
                    post = form.save(commit=False)
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
            return render(request, 'hospital/add-profile.html', {
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
                form = AddHospitalProfileForm(
                    request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    form.save()
                    return redirect(reverse('hospital:hospital'))
                else:
                    return render(request, 'hospital/add-profile.html', {
                        'form': form,
                        'error': True,
                    })

            return render(request, 'hospital/add-profile.html', {
                'form': form,
                'error': False,
            })
        except ObjectDoesNotExist:
            return redirect('coreapp:home')


def AddDoctor(request):
    if request.user.is_authenticated and request.user.role == 'HOSPITAL':
        try:
            instance = request.user.hospital
            form = DoctorForm(instance=instance)
            if request.method == "POST":
                form = DoctorForm(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    form.save()
                    return redirect(reverse('hospital:doctor_profile'))
                else:
                    return render(request, 'hospital/add-doctor.html', {
                        'form': form,
                        'error': True,
                    })

            return render(request, 'hospital/add-doctor.html', {
                'form': form,
                'error': False,
            })
        except ObjectDoesNotExist:
            
            return redirect('hospital:hospital')
    else:
        return redirect('login')
    
def EditDoctor(request, doctor_id):
    if request.user.is_authenticated and request.user.role == 'HOSPITAL':
        doctor = Doctor.objects.get(id=doctor_id)
        if doctor.hospital == request.user.hospital:
            form = DoctorForm(instance=doctor)
            if request.method == "POST":
                form = DoctorForm(request.POST, request.FILES, instance=doctor)
                if form.is_valid():
                    form.save()
                    return redirect('hospital:doctor_profile')
                else:
                    return render(request, 'hospital/add-doctor.html', {
                        'form': form,
                        'error': True,
                    })
            return render(request, 'hospital/add-doctor.html', {
                'form': form,
                'error': False,
            })
        else:
            return redirect('hospital:doctor_profile')    
def DoctorProfile(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        raise Http404("Doctor does not exist.")
    context = {
        "doctor": doctor

    }

    return render(request, 'hospital/doctor-profile.html', context)


def DoctorList(request):
    doctor = Doctor.objects.all().filter(hospital=request.user)
    context = {
        "doctors": doctor
    }
    return render(request, 'hospital/doctor-list.html', context)
