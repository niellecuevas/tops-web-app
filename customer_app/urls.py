from django.urls import path
from . import views

urlpatterns = [
    path('customerhomepage/', views.customerhomepage, name='customerhomepage'),  
    
]
