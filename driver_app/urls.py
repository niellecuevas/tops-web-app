from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.driver_login, name='driver_login'),
    path('dashboard/<str:driver_id>/', views.driver_dashboard, name='driver_dashboard'),
    path('logout/', views.driver_logout, name='logout'),
    path('my_vans/<str:driver_id>/', views.driver_my_vans, name='driver_my_vans'),

]
