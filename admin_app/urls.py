from django.urls import path
from . import views
from .views import driver_management
from .views import admin_bookings
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard view        # View for bookings
    path('statistics/', views.statistics_view, name='statistics'),          # View for statistics
    path('login/', views.admin_login, name='login'),  # Admin login view
    path('admin_logout/', views.logout, name='admin_logout'), 
    path('driver_management/', driver_management, name='driver_management'),
    path('destination/', views.destination, name='destination'), 
    path('admin_bookings/', admin_bookings, name='admin_bookings'),
    path('confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
     path('confirm_custom_booking/<int:booking_id>/', views.confirm_custom_booking, name='confirm_custom_booking'),
    path('update-driver/', views.updateDriverForm, name='update_driver'),
    path('driver_management/delete/<str:driver_id>/', views.delete_driver, name='delete_driver'),
    path('van_management/', views.van_management, name='van_management'),  
    path('vans/delete/<int:van_id>/', views.delete_van, name='delete_van'),
    path('vans/update/<int:van_id>/', views.update_van, name='update_van'),
    path('destination/update/<int:destination_id>/', views.update_destination, name='update_destination'),
    path('destination/delete/<int:destination_id>/', views.delete_destination, name='delete_destination'),
]
