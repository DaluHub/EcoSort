from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('request_pickup/', views.request_pickup_view, name='request_pickup'),
    path('my_activity/', views.my_activity_view, name='my_activity'),
]