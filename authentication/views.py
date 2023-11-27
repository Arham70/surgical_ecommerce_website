# myapp/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .form import ProfileSetupForm
from .models import CustomUser


def SignUpPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your Password and confirm password do not match!!")
        else:
            # Create a user without the additional attributes
            my_user = CustomUser.objects.create_user(username=uname, email=email, password=pass1)
            my_user.save()

            # Redirect to profile setup page with user ID in the URL
            return redirect('login')

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('signup')  # Redirect to user profile or another page
        else:
            return HttpResponse("Username or Password is incorrect!!")

    return render(request, 'login.html')


@login_required
def profile_setup(request):
    user = request.user  # This gets the currently logged-in user
    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('proceed_to_checkout')  # Redirect to the checkout page after profile setup
    else:
        form = ProfileSetupForm(instance=user)

    return render(request, 'profile_setup.html', {'form': form})


@login_required
def UserProfile(request):
    return render(request, 'user_profile.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')