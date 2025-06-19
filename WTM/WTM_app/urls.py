from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('contact/', views.contact_view, name='contact'),
    path('upgrade-request/', views.upgrade_request_view, name='upgrade_request'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('companies/', views.company_list_view, name='company_list'),
    path('request_pickup/', views.request_pickup_view, name='request_pickup'),
    path('my_activity/', views.my_activity_view, name='my_activity'),
    path('rewards/', views.rewards_view, name='rewards'),
    path('redeem/', views.redeem_view, name='redeem'),
    path('transactions/', views.transactions_view, name='transactions'),
    path('customer_care/', views.customer_care_view, name='customer_care'),
    path('report_issue/', views.report_issue_view, name='report_issue'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]