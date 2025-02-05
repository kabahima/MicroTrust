
from django.shortcuts import render, redirect
from .forms import MemberRegistrationForm



def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save()
           
            return redirect('home')
    else:
        form = MemberRegistrationForm()
    
    return render(request, 'members/register.html', {'form': form})
