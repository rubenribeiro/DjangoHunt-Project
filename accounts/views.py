from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth 

# Create your views here.

def signup(request):
    if request.method == 'POST':
        # If it's a post user sent an account creation request
        if request.POST['password1'] == request.POST['password2']:
            try:
                #This will rase an User.DoesNotExit exception if user doesn't exit
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error':'Username has already been taken'})
            except User.DoesNotExist:
                #create an user account, login and send he/she back to home page
                user =  User.objects.create_user(request.POST['username'], password=request.POST['password1'])                
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error':'Password must match'})

    else:
        # User wants to enter info
        return render(request, 'accounts/signup.html') 

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid Username or Password.'}) 

    else:
        return render(request, 'accounts/login.html')

def logout(request):
    # Do a POST logout Do to some issues with browsers
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
