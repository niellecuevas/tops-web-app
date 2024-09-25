from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard view
    path('bookings/', views.bookings, name='bookings'),                # View for bookings
    path('statistics/', views.statistics, name='statistics'),          # View for statistics
]
