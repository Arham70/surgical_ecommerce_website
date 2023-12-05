# myapp/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import RequestProductForm
from .form import ProfileSetupForm, ProductForm
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
            return redirect('profile_setup')  # Redirect to user profile or another page
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
