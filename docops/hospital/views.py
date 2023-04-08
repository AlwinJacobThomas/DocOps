from django.shortcuts import render,reverse,redirect

# Create your views here.




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
        return render(request, 'hospital/landing.html')