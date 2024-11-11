from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.driver_login, name='driver_login'),
    path('dashboard/<str:driver_id>/', views.driver_dashboard, name='driver_dashboard'),
    path('drivermyvan/<str:driver_id>', views.drivermyvan, name='drivermyvan'),
    path('logout/', views.driver_logout, name='logout'),

]
