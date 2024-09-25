from django.shortcuts import render

def customerhomepage(request):
    return render(request, 'customer_app/customerhomepage.html') 