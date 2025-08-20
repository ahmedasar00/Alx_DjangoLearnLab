from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username= form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            login(request,user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request,'registration/register.html', {'form':form})

def user_login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username , password = password)
        if user is not None:
            login(request,user)
            return redirect('porfile')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    messages.info(request,'you have been logged out.')
    return redirect('login')


@login_required 
def profile(request):
    if  request.method == 'POST':
        email = request.POST['email']
        request.user.email = email
        request.user.save()
        messages.success(request, 'profile updated successfully!')
        return redirect('profile')
    return render(request, 'registration/profile.html')