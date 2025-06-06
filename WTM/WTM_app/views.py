from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, WastePickupRequestForm, CustomAuthenticationForm
from .models import WastePickupRequest

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Change 'home' to your homepage url name
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def request_pickup_view(request):
    if request.method == 'POST':
        form = WastePickupRequestForm(request.POST)
        if form.is_valid():
            pickup = form.save(commit=False)
            pickup.user = request.user
            pickup.save()
            return redirect('my_activity')
    else:
        form = WastePickupRequestForm()
    return render(request, 'request_pickup.html', {'form': form}) 

@login_required
def my_activity_view(request):
    pickup_requests = WastePickupRequest.objects.filter(user=request.user)
    return render(request, 'my_activity.html', {'pickup_requests': pickup_requests})   