from django.urls import path
from . import views

app_name = 'driver_app'

urlpatterns = [
    path('dashboard/<str:driver_id>/', views.driver_dashboard, name='driver_dashboard'),
    path('logout/', views.driver_logout, name='logout'),
    path('my_vans/<str:driver_id>/', views.driver_my_vans, name='driver_my_vans'),
    path('my_vans/<str:driver_id>/update_availability/<int:van_id>/', views.update_availability, name='update_availability'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.driver_login, name='driver_login'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),  # Update with the actual name of your dashboard view
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
