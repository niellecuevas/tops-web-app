from django.urls import path
from . import views

urlpatterns = [
    path('customerhomepage/', views.customerhomepage, name='customerhomepage'),  
    path('cstmrbookingdetails/', views.cstmrbookingdetails, name='cstmrbookingdetails'),
    path('customerform/', views.load_customer_form, name='customerform'),
]
