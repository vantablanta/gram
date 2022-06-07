from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from gram_app.models import Image, Comment, Profile, Likes
from .forms import RegisterForm, AddImageForm, UpdateImageForm, UpdateProfileForm
from .emails import send_welcome_email


def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User doesnt exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password doesnt exist')
    context = {'page': page}
    return render(request, 'gram_app/login-register.html', context)


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
            recipient = User(username=username, email=email)
            send_welcome_email(username, email)

            profile = Profile.objects.create(name=username, owner=user)
            profile.save()

            return render(request, 'gram_app/register-success.html')

    context = {'page': page, 'form': form}
    return render(request, 'gram_app/login-register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='')
def home(request):
    images = Image.objects.all()
    profile = request.user
    profile_info = Profile.objects.get(owner=profile)
    context = {'images': images, 'profile_info': profile_info, }
    return render(request, 'gram_app/index.html', context)

@login_required(login_url='')
def search(request):
    query = request.GET.get('q')
    if query:
        images = Image.objects.filter(
            Q(image_name__icontains=query) |
            Q(owner__name__icontains=query) |
            Q(image_caption__icontains=query)
        )
        context = {'images': images}
        return render(request, 'gram_app/search.html', context)
        
@login_required(login_url='')
def upload_images(request):
    form = AddImageForm()
    user = request.user
    owner = Profile.objects.get(owner=user)
    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_name = form.cleaned_data['image_name']
            image_caption = form.cleaned_data['image_caption']
            upload = Image(image=image, image_name=image_name,
                           image_caption=image_caption, owner=owner)
            upload.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'gram_app/upload.html', context)

@login_required(login_url='')
def delete_image(request, pk):
    image = Image.objects.get(id=pk)
    if request.method == "POST":
        image.delete()
        return redirect('home')
    return render(request, 'gram_app/delete.html', {'obj': image})

@login_required(login_url='')
def update_image(request, pk):
    image = Image.objects.get(id=pk)
    form = UpdateImageForm(request.POST or None, instance=image)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.owner = request.user.profile
            form.instance.image = image.image
            form.instance.image_name = image.image_name
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'gram_app/update.html', context)

@login_required(login_url='')
def comments(request, pk):
    image = Image.objects.get(id=pk)
    comments = Comment.objects.filter(image=image)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        print(comment)
        comment_owner = Profile.objects.get(owner=request.user)
        new_comment = Comment.objects.create(
            comment=comment, image=image, owner=comment_owner)
        new_comment.save()

    context = {'comment': comments, 'image': image}
    return render(request, 'gram_app/comments.html', context)

@login_required(login_url='')
def profiles(request):
    user = request.user
    profile = Profile.objects.get(owner=user)
    images = Image.objects.filter(owner=profile)
    context = {'profile': profile, 'images': images}
    return render(request, 'gram_app/profile.html', context)

def update_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    form = UpdateProfileForm(request.POST, instance=profile)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {'form': form}
    return render(request, 'gram_app/update.html', context)


def like(request, pk):
        user = request.user
        image = Image.objects.get(id=pk)
        current_likes = image.likes
        liked = Likes.objects.filter(user=user, image=image).count()

        if not liked:
            like = Likes.objects.create(user=user, image=image)
            current_likes = current_likes + 1

        else:
            Likes.objects.filter(user=user, image=image).delete()
            current_likes = current_likes - 1

        image.likes = current_likes
        image.save()

        return HttpResponseRedirect(reverse('home'))