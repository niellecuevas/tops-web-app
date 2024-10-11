from django.urls import path
from . import views


urlpatterns = [
    path('customerhomepage/', views.customerhomepage, name='customerhomepage'),  
    path('cstmrbookingdetails/', views.cstmrbookingdetails, name='cstmrbookingdetails'),
    path('customerform/', views.customer_form_view, name='customerform'),
    path('success/', views.success, name='success'),
    path('customerhomepage2/', views.customerhomepage2_view, name='customerhomepage2'),
    path('bookvan/', views.bookvan, name='bookvan'),
]
