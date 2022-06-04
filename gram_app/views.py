from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.contrib import messages
from .forms import RegisterForm
from .emails import send_welcome_email

def loginUser(request):
    page='login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User doesnt exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password doesnt exist')
    context = {'page':page}
    return render(request, 'gram_app/login-register.html',context )

def registerUser(request):
    form = RegisterForm()
    page = 'register'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            recipient = User(username = username,email =email)
            send_welcome_email(username,email)


            return HttpResponse('User created')
    context = {'page': page, 'form': form}
    return render(request, 'gram_app/login-register.html',context )

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='')
def home(request):
    context = {}
    return render(request, 'gram_app/index.html', context)


