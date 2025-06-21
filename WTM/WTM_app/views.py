from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, TestimonialForm, UpgradeRequestForm, WastePickupRequestForm, CustomAuthenticationForm
from .models import Testimonial, WastePickupRequest, Company, Hero, FeatureCard, UpgradeRequest
from django.db.models import Sum

def home_view(request):
    hero = Hero.objects.first()
    features = FeatureCard.objects.all()
    # Example stats (replace with your actual model/fields if different)
    total_users = 0
    total_pickups = 0
    total_waste_recycled = 0
    total_rewards_redeemed = 0
    try:
        from .models import CustomUser, WastePickupRequest, Reward
        total_users = CustomUser.objects.count()
        total_pickups = WastePickupRequest.objects.count()
        total_waste_recycled = WastePickupRequest.objects.aggregate(Sum('waste_weight'))['waste_weight__sum'] or 0
        total_rewards_redeemed = Reward.objects.count()
    except Exception:
        pass  # fallback if models are not available

    testimonials = Testimonial.objects.filter(approved=True).order_by('-created_at')[:6]

    return render(request, 'home.html', {
        'hero': hero,
        'features': features,
        'total_users': total_users,
        'total_pickups': total_pickups,
        'total_waste_recycled': total_waste_recycled,
        'total_rewards_redeemed': total_rewards_redeemed,
        'testimonials': testimonials,
    })


def about_view(request):
    return render(request, 'about.html')

def services_view(request):
    return render(request, 'pages/services.html')

def contact_view(request):
    return render(request, 'contact.html')

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
def dashboard_view(request):
    # Render dashboard template
    return render(request, 'dashboard.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Change 'home' to your homepage url name
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})



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

            # --------- EMAIL SENDING CODE STARTS HERE ----------
            from django.core.mail import EmailMessage
            from django.template.loader import render_to_string

            # Email to user
            subject = "Your Upgrade Request was Received"
            html_message = render_to_string('upgrade/email_requested.html', {'user': request.user, 'upgrade': upgrade})
            user_email = EmailMessage(subject, html_message, to=[request.user.email])
            user_email.content_subtype = "html"
            user_email.send()

            # Email to admin
            admin_subject = "New Upgrade Request Submitted"
            admin_html = render_to_string('upgrade/email_admin_notify.html', {'user': request.user, 'upgrade': upgrade})
            admin_email = EmailMessage(admin_subject, admin_html, to=['your_admin_email@example.com'])  # <-- change to your real email
            admin_email.content_subtype = "html"
            admin_email.send()
            # --------- EMAIL SENDING CODE ENDS HERE ----------

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


@login_required
def submit_testimonial_view(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(request, "Thank you! Your testimonial will appear after approval.")
            return redirect('home')
    else:
        form = TestimonialForm()
    return render(request, 'submit_testimonial.html', {'form': form})

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