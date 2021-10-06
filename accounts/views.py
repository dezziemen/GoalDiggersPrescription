from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from .forms import CreateUserForm, PatientRegisterForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser


# Create user function for superuser (login required)
@login_required(login_url='/login/')
def create_user(request):
    # If not logged in or not admin, go home
    if not request.user.is_authenticated or not request.user.user_type == 'admin':
        return redirect('home')
    # If trying to submit form
    if request.method == 'POST':
        # Create form
        form = CreateUserForm(request.POST)
        # After saving form, go to home page
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreateUserForm()
    return render(request, 'admin/create_user.html', {"form": form})


# Register new patient
def register(request):
    # If user is logged in, go home
    if request.user.is_authenticated:
        return redirect('home')
    # If POST
    if request.method == 'POST':
        # Create register form with entered details
        form = PatientRegisterForm(request.POST)
        # If form is valid
        if form.is_valid():
            # Get form, don't save
            user = form.save(commit=False)
            # Set user type to patient
            user.user_type = 'patient'
            # Save form
            form.save()
            # Login registered user
            login(request, user)
            return redirect('home')
    # Get new form
    else:
        form = PatientRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# Login for all users
def login_view(request):
    # If logged in, go home
    if request.user.is_authenticated:
        return redirect('home')
    # If POST
    if request.method == 'POST':
        # Create login form with entered details
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # If redirected from elsewhere, go to page
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            # Else, go home
            else:
                return redirect('home')
    # Get new form
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


# Logout
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
