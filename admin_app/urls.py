from django.urls import path
from . import views
from .views import driver_management

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard view
    path('bookings/', views.bookings, name='bookings'),                # View for bookings
    path('statistics/', views.statistics, name='statistics'),          # View for statistics
    path('login/', views.admin_login, name='login'),  # Admin login view
    path('admin_logout/', views.logout, name='admin_logout'), 
    path('driver_management/', driver_management, name='driver_management'), 
]
