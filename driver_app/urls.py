from django.urls import path
from . import views

urlpatterns = [
    path('driverdashboard/', views.driverdashboard, name='driverdashboard'),  
    path('driverlogin/', views.driverlogin, name='driverlogin'),  
    
]
