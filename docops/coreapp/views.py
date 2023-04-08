from django.shortcuts import render,redirect,reverse

from django.contrib.auth.decorators import login_required
# Create your views here.


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
def c_dash(request):
    return render(request, 'coreapp/c-dash.html')
@login_required
def p_dash(request):
    return render(request, 'coreapp/p-dash.html')

@login_required
def profile(request):
    return render(request, 'coreapp/profile.html')
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
    return render(request, 'coreapp/hos-search.html')



