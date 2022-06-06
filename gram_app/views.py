from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.contrib import messages
from gram_app.models import Image, Comment, Profile
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

            profile = Profile.objects.create(name =username, owner = user)
            profile.save()

            return HttpResponse('User created')
    context = {'page': page, 'form': form}
    return render(request, 'gram_app/login-register.html',context )

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='')
def home(request):
    images  = Image.objects.all()
    profile = request.user
    profile_info = Profile.objects.get(owner=profile)
    context = {'images':images, 'profile_info':profile_info, 'comments':comments}
    return render(request, 'gram_app/index.html', context)

@login_required(login_url='')
def comments(request, pk):
    image = Image.objects.get(id=pk)
    comments = Comment.objects.filter(image = image)
    context = {'comment': comments, 'image':image} 
    return render(request, 'gram_app/comments.html', context )

@login_required(login_url='')
def add_comments(request, pk):
    image = get_object_or_404(Image, id=pk)
    if request.method == 'POST':
        comment  = request.POST.get('comments')
        print(comment)
        new_comment = Comment.objects.create(comment= comment, image=image, owner = request.user)
        new_comment.save()
    context = {} 
    return render(request, 'gram_app/comments.html', context )

@login_required(login_url='')
def profiles(request):
    user = request.user
    profile  = Profile.objects.get(owner=user)
    images = Image.objects.filter(owner=profile)
    context = {'profile': profile, 'images': images}
    return render(request, 'gram_app/profile.html', context)