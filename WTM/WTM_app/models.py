from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


# 1. Custom User model with roles
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('customer_care', 'Customer Care'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Hero(models.Model):
    heading = models.CharField(max_length=200)
    subtext = models.TextField()
    button_text = models.CharField(max_length=50, default="Join Us")
    button_link = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.heading


class FeatureCard(models.Model):
    title = models.CharField(max_length=100)
    tag_line = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='feature_images/')
    alt_text = models.CharField(max_length=100)

    def __str__(self):
        return self.title


User = get_user_model()
class UpgradeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Company Information
    company_name = models.CharField(max_length=100, default='Company Name')
    registration_number = models.CharField(max_length=100, default='none')
    tax_id = models.CharField(max_length=100, default='none')
    business_type = models.CharField(max_length=100, default='Waste Management')
    contact_name = models.CharField(max_length=255, default='Primary Contact')
    contact_email = models.EmailField(max_length=50, default='email')
    contact_phone = models.CharField(max_length=20, default='none')
    street_address = models.CharField(max_length=255, default='none')
    city = models.CharField(max_length=100, default='City Name')
    state = models.CharField(max_length=100, default='State Name')
    postal_code = models.CharField(max_length=20, default='Postal Code')
    country = models.CharField(max_length=100, default='Country Name')
    waste_type = models.CharField(max_length=255, default='none')
    service_areas = models.TextField(default='Service Areas', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    years_in_operation = models.PositiveIntegerField(default=1)
    num_employees = models.PositiveIntegerField(default=1)
    certifications = models.TextField(blank=True)
    sustainability_practices = models.TextField(blank=True)
    terms_agreed = models.BooleanField(max_length=100, default=True)
    privacy_agreed = models.BooleanField(max_length=100, default=True)
    justification = models.TextField(max_length=500, blank=True, null=True)
    approved = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Upgrade Request"

    def notify_admin(self):
        subject = f"New Upgrade Request from {self.user.username}"
        html_message = render_to_string('upgrade/email_admin_notify.html', {'user': self.user, 'upgrade': self})
        admin_email = settings.DEFAULT_FROM_EMAIL  # Or your admin email directly
        email = EmailMessage(subject, html_message, to=[admin_email])
        email.content_subtype = "html"
        email.send()

    def notify_user(self, status):
        if status == 'approved':
            subject = "Your Upgrade Request Has Been Approved"
            template = 'upgrade/email_approved.html'
        elif status == 'declined':
            subject = "Your Upgrade Request Was Rejected"
            template = 'upgrade/email_rejected.html'
        else:
            subject = "Your Upgrade Request was Received"
            template = 'upgrade/email_requested.html'
        html_message = render_to_string(template, {'user': self.user, 'upgrade': self})
        email = EmailMessage(subject, html_message, to=[self.user.email])
        email.content_subtype = "html"
        email.send()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not is_new:
            previous = UpgradeRequest.objects.get(pk=self.pk)
        super().save(*args, **kwargs)
        if is_new:
            self.notify_admin()
            self.notify_user('submitted')
        else:
            previous = UpgradeRequest.objects.get(pk=self.pk)
            if not previous.approved and self.approved:
                self.notify_user('approved')
            elif not previous.declined and self.declined:
                self.notify_user('declined')
                
class Testimonial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField("Testimonial")
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # Only show approved testimonials

    def __str__(self):
        return f"{self.user.username}: {self.text[:30]}"


# contact page 
class ContactPage(models.Model):
    hero_title = models.CharField(max_length=100, default="Contact Us")
    hero_subtitle = models.CharField(max_length=255, default="Smart Waste Disposal for a Cleaner Future")
    hero_image = models.ImageField(upload_to="contact_hero/")

    contact_heading = models.CharField(max_length=100, default="We are always ready to help you and answer your questions")
    contact_message = models.TextField(default="Whether you have a question, a suggestion, or just want to say hello...")

    open_days = models.CharField(max_length=100, default="Monday - Friday 08.00 – 18.00")
    address = models.CharField(max_length=255, default="100 S Main St, New York, NY")
    phone = models.CharField(max_length=20, default="+1 123 456 789")
    email = models.EmailField(default="contact@ecosort.com")

    def __str__(self):
        return "Contact Page Content"

class Footer(models.Model):
    logo = models.ImageField(upload_to='footer/')
    about_text = models.TextField()

    # Company links
    company_home = models.CharField(max_length=255, blank=True, null=True)
    company_about = models.CharField(max_length=255, blank=True, null=True)
    company_services = models.CharField(max_length=255, blank=True, null=True)
    company_contact = models.CharField(max_length=255, blank=True, null=True)

    # Services links
    service1 = models.CharField(max_length=100, default="Waste Collection")
    service2 = models.CharField(max_length=100, default="Waste Recycling")
    service3 = models.CharField(max_length=100, default="Waste to Rewards")
    service4 = models.CharField(max_length=100, default="Recycling Education")
    service5 = models.CharField(max_length=100, default="EcoSort Support")
    service6 = models.CharField(max_length=100, default="Medical Waste")

    # Newsletter
    newsletter_text = models.CharField(max_length=255, default="Your email is safe with us. We don’t spam.")

    # Social Links
    facebook = models.URLField(default="#")
    twitter = models.URLField(default="#")
    linkedin = models.URLField(default="#")
    youtube = models.URLField(default="#")
    whatsapp = models.URLField(default="#")

    def __str__(self):
        return "Footer Content"

# 2. Company model
class Company(models.Model):
    STATUS_CHOICES = (
        ('upgrade', 'Upgrade'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    contact_email = models.EmailField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class CompanyRating(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1 to 5
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# 3. WastePickupRequest model
class WastePickupRequest(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='pickup_requests')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='pickup_requests')
    address = models.CharField(max_length=255)
    scheduled_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.company.name} ({self.status})"

# service page
class Service(models.Model):
    icon = models.CharField(max_length=100, help_text="Font Awesome class, e.g. 'fas fa-recycle'")
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class WhyChooseUs(models.Model):
    icon = models.CharField(max_length=100, help_text="Font Awesome class")
    title = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.title

class ServiceStep(models.Model):
    icon = models.CharField(max_length=100, help_text="Step number or icon")
    title = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.title

class ServicePageContent(models.Model):
    hero_title = models.CharField(max_length=150, default="EcoSort Recycling Services")
    hero_subtitle = models.CharField(max_length=255, default="Innovative, Sustainable, Community-Driven")
    hero_desc = models.TextField(default="Discover how EcoSort is transforming waste management and recycling for a cleaner, greener future.")
    cta_text = models.CharField(max_length=120, default="Ready to Make a Difference?")
    cta_btn = models.CharField(max_length=40, default="Join EcoSort Now")
    footer_text = models.CharField(max_length=120, default="© 2025 EcoSort | All rights reserved.")

    def __str__(self):
        return "Service Page Content"

# models.py
class ActivityPageContent(models.Model):
    title = models.CharField(max_length=100, default="My Activity")
    subtitle = models.CharField(max_length=200, default="Track your recycling journey and impact.")
    stats_title = models.CharField(max_length=100, default="Your Eco Stats")
    activity_title = models.CharField(max_length=100, default="Recent Activity")
    empty_message = models.CharField(max_length=200, default="You haven't made any pickup requests yet. Start recycling today!")
    cta_request = models.CharField(max_length=100, default="Request a Pickup")
    cta_rewards = models.CharField(max_length=100, default="View My Rewards")
    goal_label = models.CharField(max_length=100, default="Monthly Recycling Goal")
    goal_kg = models.PositiveIntegerField(default=50)

    def __str__(self):
        return "Activity Page Content"

    

# 4. Reward/Token model
class Reward(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rewards')
    tokens = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tokens} tokens"

# 5. Transaction model
class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tokens_redeemed = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({'Approved' if self.is_approved else 'Pending'})"