# myapp/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pyexpat.errors import messages

from .models import RequestProductForm
from .form import ProfileSetupForm, ProductForm, PasswordResetRequestForm
from .models import CustomUser


def SignUpPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            # Check if the email already exists
            if CustomUser.objects.filter(email=email).exists():
                return render(request, 'signup.html', {'error': 'Email already exists'})

            # Create the user
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
             # Log the user in after successful registration
            return redirect('login')  # Redirect to the home page or any desired URL
        else:
            # Handle password mismatch error
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile_setup')  # Redirect to the home page or any desired URL
        else:
            # Handle login failure
            return render(request, 'login.html', {'error': 'Invalid login credentials'})

    return render(request, 'login.html')


@login_required
def profile_setup(request):
    user = request.user  # This gets the currently logged-in user
    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return render(request, 'index.html')  # Redirect to the checkout page after profile setup
    else:
        form = ProfileSetupForm(instance=user)

    return render(request, 'profile_setup.html', {'form': form})


@login_required
def UserProfile(request):
    return render(request, 'user_profile.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'index.html')


def ContactUs(request):
    return render(request, 'ContactUs.html')


def AboutUs(request):
    return render(request, 'About_us.html')


def FAQS(request):
    return render(request, 'Faqs.html')


def PaymentMethod(request):
    return render(request, 'PaymentMethod.html')


def deliveryInformation(request):
    return render(request, 'deliveryInformation.html')


def ReturnAndRefunds(request):
    return render(request, 'ReturnAndRefunds.html')


def PrivacyPolicy(request):
    return render(request, 'PrivacyPolicy.html')


def TermsAndConditions(request):
    return render(request, 'TermsAndConditions.html')


def request_product_form(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page
    else:
        form = ProductForm()

    return render(request, 'CustomerRequest.html', {'form': form})


def blog(request):
    return render(request,'blog.html')


def success_page(request):
    return  render(request,'payment_success.html')
