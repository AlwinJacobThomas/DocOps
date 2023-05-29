from django.shortcuts import render, reverse, redirect,get_object_or_404
from .forms import AddHospitalProfileForm
from user.models import HospitalProfile
from .models import Doctor
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import DoctorForm
from django.http import Http404
from coreapp.models import Appointment,AppointmentReview
from django.http import HttpResponse

User = get_user_model()


def hospital(request):
    if request.user.is_authenticated:
        if request.user.role == 'HOSPITAL':
            try:
                hospital = request.user.hospital
                doctors = Doctor.objects.filter(hospital=hospital.user)
                print(doctors)
                return render(request, 'hospital/hos_doctors.html', {
                    'hospital': hospital,
                    'doctors': doctors
                })
            except ObjectDoesNotExist:
                return redirect(reverse('hospital:add_profile'))
        elif request.user.role == 'PATIENT':
            return redirect(reverse('coreapp:home'))
        else:
            return redirect('/admin/')

    else:
        return redirect('user:hossignup')


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
            if request.method == "POST":
                form = DoctorForm(request.POST, request.FILES)
                if form.is_valid():
                    doctor = form.save(commit=False)
                    doctor.hospital = request.user.hospital.user
                    if 'pic' in request.FILES:
                        doctor.pic = request.FILES['pic']
                    doctor.save()
                    return redirect(reverse('hospital:hos_doctors'))
                else:
                    return render(request, 'hospital/add-doctor.html', {
                        'form': form,
                        'error': True,
                        'doctors': Doctor.objects.filter(hospital=request.user)
                    })

            form = DoctorForm()
            return render(request, 'hospital/add-doctor.html', {
                'form': form,
                'error': False,
                'doctors': Doctor.objects.filter(hospital=request.user)
            })
        except ObjectDoesNotExist:
            return redirect('hospital:doctor_list')
        
def EditDoctor(request, doctor_id):
    if request.user.is_authenticated and request.user.role == 'HOSPITAL':
        doctor = get_object_or_404(Doctor, id=doctor_id)
        form = DoctorForm(request.POST or None, request.FILES or None, instance=doctor)#populate with data in form for edit form
       
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect(reverse('hospital:doctor_list'))
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
        return redirect('hospital:doctor_list')
def DeleteDoctor(request, doctor_id):
    if request.user.is_authenticated and request.user.role == 'HOSPITAL':
        doctor = Doctor.objects.get(id=doctor_id)
        doctor.delete()
        context ={
            "message":"sucessfully deleted"
        }
        return redirect(reverse('hospital:doctor_list'))
       
         
def DoctorProfile(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        raise Http404("Doctor does not exist.")
    context = {
        "doctor": doctor
    }

    return render(request, 'hospital/doctor-profile.html', context)

@login_required
def HosAppointmentsView(request):
    appointments = Appointment.objects.filter(hospital=request.user)

    cancelled_appoinments = appointments.filter(appointment_status='cancelled')
    completed_appoinments = appointments.filter(appointment_status='completed')
    pending_appoinments = appointments.filter(appointment_status='pending')
    return render(request, 'hospital/hos_appointments.html', {
        'cancelled_appointments': cancelled_appoinments,
        'completed_appointments': completed_appoinments,
        'pending_appointments': pending_appoinments
    })

@login_required
def HosAppointmentConfirmView(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        if request.method == 'POST' and request.POST.get('_method') != 'DELETE':
            appointment.appointment_status = 'completed'
            appointment.save()
            return HttpResponse("Appointment marked as completed.")
        
        if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
            appointment.appointment_status = 'cancelled'
            appointment.save()
            return HttpResponse("Appointment cancelled.")

    except ObjectDoesNotExist:
        return HttpResponse("Appointment not found.")
    
    return HttpResponse("Invalid request.")

def HosDoctorsView(request):
    doctor = Doctor.objects.all().filter(hospital=request.user)
    context = {
        "doctors": doctor
    }
    return render(request, 'hospital/hos_doctors.html', context)