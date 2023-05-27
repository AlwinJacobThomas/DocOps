from django.shortcuts import render,redirect,reverse
from .forms import AddPatientProfileForm,AppointmentReviewForm, AppointmentBookingForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from user.models import HospitalProfile
from hospital.models import Doctor
from .models import Appointment, AppointmentReview
from django.http import HttpResponse
from django.db.models import Avg
# from docops.lstm2 import predict_star_rating, load_model, tokenizer
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
User = get_user_model()

@login_required
def home(request):
    if request.user.is_authenticated:
        if request.user.role=='HOSPITAL':
            return redirect(reverse('hospital:hospital'))
        else:
            return render(request, 'coreapp/u-dash.html', {
                'pending': Appointment.objects.filter(appointment_status='pending').order_by('-id'),
            })
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
def p_dash(request):
    if request.user.is_authenticated:
        if request.user.role=='HOSPITAL':
            return redirect(reverse('hospital:hospital'))
        else:
            reviewed_appointments = Appointment.objects.filter(appointment_review__appointment__patient=request.user.patient.user, appointment_status='completed')
            not_reviewed_appointments = Appointment.objects.filter(appointment_status='completed').exclude(appointment_review__appointment__patient=request.user.patient.user)

            completed = {
                'reviewed_appointments': reviewed_appointments,
                'not_reviewed_appointments': not_reviewed_appointments
            }
            return render(request, 'coreapp/p-dash.html', {
                'completed': completed,
            })
    else:
        return render(request, 'coreapp/landing.html')

@login_required
def c_dash(request):
    if request.user.is_authenticated:
        if request.user.role=='HOSPITAL':
            return redirect(reverse('hospital:hospital'))
        else:
            return render(request, 'coreapp/c-dash.html', {
                'cancelled': Appointment.objects.filter(appointment_status='cancelled').order_by('-id')
            })
    else:
        return render(request, 'coreapp/landing.html')

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
    if request.user.is_authenticated and request.user.role == 'PATIENT':
        doctors = Doctor.objects.all()
        context = {
            "doctors": doctors,
        }
        return render(request, 'coreapp/doc/doc-search.html', context)
    else:
        return HttpResponse("Unauthorized", status=401)

@login_required
def DoctorProfile(request,doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    reviews = AppointmentReview.objects.filter(appointment__doctor=doctor)
    rating = reviews.aggregate(avg_rating=Avg('doctor_rating'))['avg_rating']
    context = {
            "doctor":doctor,
            "reviews": reviews,
            "rating": rating                          
        }
    return render(request, 'coreapp/doc/doc-detail.html',context)


@login_required
def hos_search(request):
    if request.user.is_authenticated and request.user.role == 'PATIENT':
        hospitals = HospitalProfile.objects.all()
        context = {
            "hospitals": hospitals,
        }
        return render(request, 'coreapp/hos/hos-search.html', context)
    else:
        return HttpResponse("Unauthorized", status=401)

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
def DoctorDetailView(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'coreapp/doctor_detail.html', {
        'doctor': doctor,
        'doctor_id': doctor_id
    })

    
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
            return HttpResponse("Invalid data", status=401)
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
    reviewed_appointments = Appointment.objects.filter(appointment_review__appointment__patient=request.user.patient.user)
    if appointment.appointment_status == 'completed' and appointment not in reviewed_appointments:
        if request.method == 'POST':
            # model, tokenizer = load_model()

            hos_review = request.POST.get('hos_review')
            doc_review = request.POST.get('doc_review')

            appointmentReview = AppointmentReview(
                hospital_review = hos_review,
                # hospital_rating = float(predict_star_rating(hos_review, model, tokenizer)*5),
                doctor_review = doc_review,
                # doctor_rating = float(predict_star_rating(doc_review, model, tokenizer)*5),
                appointment = appointment
            )
            appointmentReview.save()
            # print(predict_star_rating(doc_review,model,tokenizer)*5)
            return redirect(reverse('coreapp:doctor_detail', kwargs={'doctor_id': appointment.doctor.id}))
        return render(request, 'coreapp/treatment_review.html', {
            'appointment_id': appointment_id,
            'doctor_id': appointment.doctor.id
        })
    else:
        return HttpResponse("Error", status=401)

@login_required
def HosProfile(request, hospital_id):
    appointments = Appointment.objects.filter(hospital=request.user)

    cancelled_appoinments = appointments.filter(appointment_status='cancelled')
    completed_appoinments = appointments.filter(appointment_status='completed')
    pending_appoinments = appointments.filter(appointment_status='pending')
    return render(request, 'coreapp/hos_profile.html', {
        'cancelled_appointments': cancelled_appoinments,
        'completed_appointments': completed_appoinments,
        'pending_appointments': pending_appoinments
    })

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Appointment

@login_required
def AppointmentConfirm(request, appointment_id):
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
