from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UpgradeRequestForm, WastePickupRequestForm, CustomAuthenticationForm
from .models import WastePickupRequest, Company, Hero, FeatureCard, UpgradeRequest

def home_view(request):
    hero = Hero.objects.first()
    features = FeatureCard.objects.all()
    return render(request, 'home.html', {'hero': hero, 'features': features})

def about_view(request):
    return render(request, 'about.html')

def services_view(request):
    return render(request, 'services.html')

def contact_view(request):
    return render(request, 'contact.html')
    
@login_required
def dashboard_view(request):
    # Render dashboard template
    return render(request, 'dashboard.html')

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
            return redirect('dashboard')  # Change 'dashboard' to your dashboard url name
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def upgrade_request_view(request):
    existing = UpgradeRequest.objects.filter(user=request.user, approved=False, declined=False).first()
    if existing:
        return render(request, 'upgrade/already_requested.html', {'request': existing})

    if request.method == 'POST':
        form = UpgradeRequestForm(request.POST)
        if form.is_valid():
            upgrade = form.save(commit=False)
            upgrade.user = request.user
            upgrade.save()
            return render(request, 'upgrade/request_submitted.html')
    else:
        form = UpgradeRequestForm()
    return render(request, 'upgrade/request_upgrade.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
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

def company_list_view(request):
    companies = Company.objects.all()
    return render(request, 'company_list.html', {'companies': companies})     

# i will still modify am
def rewards_view(request):
    return render(request, 'rewards.html')

def redeem_view(request):
    return render(request, 'redeem.html')

def transactions_view(request):
    return render(request, 'transactions.html')

def customer_care_view(request):
    return render(request, 'customer_care.html')

def report_issue_view(request):
    return render(request, 'report_issue.html')

def feedback_view(request):
    return render(request, 'feedback.html')

def profile_view(request):
    return render(request, 'profile.html')    