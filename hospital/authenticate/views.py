from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        if User.objects.filter(email=email).exists():
                messages.info(request,"Email already in use")
                return redirect('signup')
        else:
                user = User.objects.create_user(username=username, email=email, password=password)

                # Logging in user
                user_login = auth.authenticate(username=username, email=email, password=password)
                auth.login(request, user_login)
                return redirect('/home')
    else:
        return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user=auth.authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/home')
        else:
            messages.info(request,'Authentication failed')
            return redirect('/')
    else:
        return render(request, 'signin.html')
    


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')