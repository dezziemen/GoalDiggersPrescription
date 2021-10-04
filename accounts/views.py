from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from .forms import CreateUserForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser


# Create user function for superuser (login required)
@login_required(login_url='/login/')
def create_user(request):
    # If user not logged in, redirect to login page
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    # If user not superuser, redirect to home
    elif not CustomUser.objects.get(pk=request.user.pk).is_superuser:
        return redirect('home')
    #
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')

    else:
        form = CreateUserForm()
    return render(request, 'admin/create_user.html', {"form": form})


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:login')

    else:
        form = CreateUserForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
