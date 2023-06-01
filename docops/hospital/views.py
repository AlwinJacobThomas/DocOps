from django.shortcuts import render, reverse, redirect, get_object_or_404
from .forms import AddHospitalProfileForm,FacilityForm

from .models import Doctor,Facility
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import DoctorForm
from django.http import Http404
from coreapp.models import Appointment, AppointmentReview
from django.http import HttpResponse
from django.contrib import messages

User = get_user_model()


def hos_dashboard(request):
    if request.user.is_authenticated:
        if request.user.role == 'HOSPITAL':
            try:
                hospital = request.user.hospital
                doctors = Doctor.objects.filter(hospital=hospital.user)
                doctor_count = doctors.count()
                review_count = AppointmentReview.objects.filter(
                    appointment__hospital=hospital.user).count()
                facility = Facility.objects.all().filter(hospital=hospital.user)
                return render(request, 'hospital/hos_dashboard.html', {
                    'hospital': hospital,
                    'doctors': doctors,
                    'review_count': review_count,
                    'doctor_count': doctor_count,
                    'facilities':facility
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
                    return redirect(reverse('hospital:hos_dashboard'))
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
                    post = form.save(commit=False)
                    post.location = request.POST['location']
                    post.save()
                    return redirect(reverse('hospital:hos_dashboard'))
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
            return redirect('hospital:hos_doctors')


def EditDoctor(request, doctor_id):
    if request.user.is_authenticated and request.user.role == 'HOSPITAL':
        doctor = get_object_or_404(Doctor, id=doctor_id)
        # populate with data in form for edit form
        form = DoctorForm(request.POST or None,
                          request.FILES or None, instance=doctor)

        if request.method == "POST":

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
                })

        return render(request, 'hospital/add-doctor.html', {
            'form': form,
            'error': False,
        })
    else:
        return redirect('hospital:hos_doctors')


def DeleteDoctor(request, doctor_id):
    if request.user.is_authenticated and request.user.role == 'HOSPITAL':
        doctor = Doctor.objects.get(id=doctor_id)
        doctor.delete()
        context = {
            "message": "sucessfully deleted"
        }
        return redirect(reverse('hospital:hos_doctors'))


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


def AddFacility(request):
    form = FacilityForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            facility = form.save(commit=False)
            facility.hospital = request.user.hospital.user
            facility.save()
            return redirect('hospital:hos_dashboard') 
        else:
            form = FacilityForm()
    return render(request, 'hospital/add-facility.html', {'form':form})

def DeleteFacility(request,facility_id):
    facility = Facility.objects.get(id=facility_id)
    facility.delete()
    messages.success(request, "Successfully deleted")
    return redirect(reverse('hospital:hos_dashboard'))


