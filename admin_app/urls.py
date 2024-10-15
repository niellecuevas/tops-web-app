from django.urls import path
from . import views
from .views import driver_management
from .views import admin_bookings
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard view        # View for bookings
    path('statistics/', views.statistics, name='statistics'),          # View for statistics
    path('login/', views.admin_login, name='login'),  # Admin login view
    path('admin_logout/', views.logout, name='admin_logout'), 
    path('driver_management/', driver_management, name='driver_management'), 
    path('admin_bookings/', admin_bookings, name='admin_bookings'),
    path('update-driver/', views.updateDriverForm, name='update_driver'),
    path('van_management/', views.van_management, name='van_management'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
