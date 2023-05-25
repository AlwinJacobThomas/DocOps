from django.shortcuts import render,redirect,reverse
from .forms import AddPatientProfileForm,DoctorReviewForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from user.models import HospitalProfile
from hospital.models import Doctor,DoctorReview,Hospital
from django.shortcuts import get_object_or_404
from .models import Appointment
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
            "doctors":doctor,
                                                                
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
        form = DoctorReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.doctor_id = doctor_id
            review.user = request.user
            review.save()
            return redirect('hospital:doctor_detail', doctor_id=doctor_id)  # Redirect to doctor detail page
    else:
        form = DoctorReviewForm()
    
    return render(request, 'doc/add_review.html', {'form': form})


# F C |F F C  jupiter
# Gm Am | Gm F C

# F F | F F C 
# Gm Am | Gm F C 

# Dm C |Dm C 
# Gm Am | Gm F C  

# F C |F F C  jupiter
# Gm Am | Gm F C

# F F | F F C 
# Gm Am | Gm F C 

# Dm C |Dm C 
# Gm Am | Gm F C  

# F C |F F C  jupiter
# Gm Am | Gm F C
