from django.urls import path
from . import views
from .views import customer_homepage2 


urlpatterns = [
    path('cstmrbookingdetails/', views.cstmrbookingdetails, name='cstmrbookingdetails'),
    path('success/', views.success, name='success'),
    path('customerhomepage2/', customer_homepage2, name='customerhomepage2'), 
    path('bookvanform/', views.bookvanform, name='bookvanform'),
    path('bookdestination/', views.bookdestination, name='bookdestination'),
    path('footer/', views.footer, name='footer'),
    path('payment_summary/', views.payment_summary, name='payment_summary'),
    path('payment_summary_custom/', views.payment_summary_custom, name='payment_summary_custom'),
    path('save-booking/', views.save_booking, name='save_booking'),
    path('customisebook/', views.customisebook, name='customisebook'),
    path('van/<int:van_id>/', views.vandetail, name='vandetail'),
    path('van/<int:van_id>/book/', views.book_van, name='book_van'), 
    path('base/', views.base, name='base'),
]
