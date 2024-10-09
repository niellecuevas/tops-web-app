from django.urls import path
from . import views

urlpatterns = [
    path('customerhomepage/', views.customerhomepage, name='customerhomepage'),  
    path('cstmrbookingdetails/', views.cstmrbookingdetails, name='cstmrbookingdetails'),
    path('customerform/', views.customer_form_view, name='customerform'),
    path('success/', views.success, name='success'),
]
