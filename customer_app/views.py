from django.shortcuts import render

def customerhomepage(request):
    return render(request, 'customer_app/customerhomepage.html') 

def cstmrbookingdetails(request):
    return render(request, 'customer_app/cstmrbookingdetails.html') 

def load_customer_form(request):
    return render(request, 'customer_app/customerform.html')
