from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserChangeForm
from django.shortcuts import get_object_or_404
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import CustomUserCreationForm

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


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print(request.POST.get('first_name'))
            print(request.POST.get('last_name'))
            print("POST 데이터:", request.POST)
            print("클린 데이터:", form.cleaned_data)
            print("first_name:", form.cleaned_data.get('first_name'))
            print("last_name:", form.cleaned_data.get('last_name'))
            
            form.save()
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/signup.html', context)
@login_required
def delete(request):
    request.user.delete()
    return redirect('/')

