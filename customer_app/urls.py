from django.urls import path
from . import views
from .views import customer_homepage2 


urlpatterns = [
    path('customerhomepage/', views.customerhomepage, name='customerhomepage'),  
    path('cstmrbookingdetails/', views.cstmrbookingdetails, name='cstmrbookingdetails'),
    path('success/', views.success, name='success'),
    path('customerhomepage2/', customer_homepage2, name='customerhomepage2'),  
    path('bookvan/', views.bookvan, name='bookvan'),
    path('bookvanform/', views.bookvanform, name='bookvanform'),
    path('footer/', views.footer, name='footer'),
    path('payment_summary/', views.payment_summary, name='payment_summary'),
]
