from django.shortcuts import render,redirect,reverse
from .forms import AddPatientProfileForm,AppointmentReviewForm, AppointmentBookingForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from user.models import HospitalProfile
from hospital.models import Doctor,Hospital
from django.shortcuts import get_object_or_404
from .models import Appointment, AppointmentReview
from django.http import JsonResponse

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
    doctor = Doctor.objects.all()
    context = {
            "doctor" : doctor,
        }
    return render(request, 'coreapp/appointment.html',context)

@login_required
def booking(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        doctor_name = request.POST.get('doctor_name')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        appointment_status = request.POST.get('appointment_status')

        # Save the appointment to the database
        appointment = Appointment.objects.create(
            patient_name=patient_name,
            doctor_name=doctor_name,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            appointment_status=appointment_status
        )
        appointment.save()

        # Redirect to a success page or another URL
        return redirect('success')
    return render(request, 'coreapp/doc/booking.html')
@login_required
def doctor_booking(request):
    if request.user.is_authenticated and request.user.role == 'PATIENT':
        doctor = Doctor.objects.get()
        context = {
            'doctor':doctor
        }
    return redirect(reverse('coreapp:appointment'))   
    
@login_required
def doc_search(request):
    doctor = Doctor.objects.all()
    context = {
            "doctors":doctor,
            
        }
    return render(request, 'coreapp/doc/doc-search.html',context)

@login_required
def DoctorProfile(request,doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    context = {
            "doctor":doctor,
                                                                
        }
    return render(request, 'coreapp/doc/doc-detail.html',context)


@login_required
def hos_search(request):
    if request.user.is_authenticated and request.user.role == 'PATIENT':
        context = {
            "hospitals":HospitalProfile.objects.all(),
            "range":range(2)
        }
    return render(request, 'coreapp/hos/hos-search.html',context)


          

def AddReview(request, doctor_id):
    if request.method == 'POST':
        form = AppointmentReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.doctor_id = doctor_id
            review.user = request.user
            review.save()
            return redirect('hospital:doctor_detail', doctor_id=doctor_id)  # Redirect to doctor detail page
    else:
        form = AppointmentReviewForm()
    
    return render(request, 'doc/add_review.html', {'form': form})

@login_required
def AppointmentBookingView(request, doctor_id):
    form = AppointmentBookingForm()
    doctor = Doctor.objects.get(id=doctor_id)
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = request.user.patient.user
            appointment.hospital = doctor.hospital
            appointment.appointment_status = 'pending'
            appointment.save()
            return redirect(reverse('coreapp:appointments'))
        else:
            return JsonResponse({'message': 'Validation Failed'})
    else:
        return render(request, 'coreapp/appointment_booking.html', {
            'form': AppointmentBookingForm(),
            'doctor_id': doctor_id
        })

@login_required
def AppointmentsView(request):
    reviewed_appointments = Appointment.objects.filter(appointment_review__appointment__patient=request.user.patient.user)
    not_reviewed_appointments = Appointment.objects.exclude(appointment_review__appointment__patient=request.user.patient.user)

    completed = {
        'reviewed_appointments': reviewed_appointments,
        'not_reviewed_appointments': not_reviewed_appointments
    }

    return render(request, 'coreapp/appointments.html', {
        'pending': Appointment.objects.filter(appointment_status='pending').order_by('-id'),
        'cancelled': Appointment.objects.filter(appointment_status='cancelled').order_by('-id'),
        'completed': completed,
    })


@login_required
def TreatmentReviewView(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == 'POST':
        hos_review = request.POST.get('hos_review')
        doc_review = request.POST.get('doc_review')

        appointmentReview = AppointmentReview(
            hospital_review = hos_review,
            doctor_review = doc_review,
            appointment = appointment
        )

        appointmentReview.save()

        return redirect(reverse('coreapp:doctor_profile'))