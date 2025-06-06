from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

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