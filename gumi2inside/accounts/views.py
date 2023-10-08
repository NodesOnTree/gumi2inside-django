from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserChangeForm
from django.shortcuts import get_object_or_404
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate



# Create your views here.

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        next_url = request.GET.get('next')
        if form.is_valid():
            auth_login(request,form.get_user())
            return redirect( next_url or 'home')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form,
    }
    return render(request,'accounts/login.html',context)
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home') 

def signup(request):
    pass
@login_required
def delete(request):
    pass
@login_required
def update(request):

    if request.method =='POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form' : form,

    }
    return render(request, 'accounts/update.html', context)
@login_required
def change_password(request):
    if request.method=='POST':
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)
    context={
        'form' : form,
     
    }
    return render(request, 'accounts/change_password.html', context)