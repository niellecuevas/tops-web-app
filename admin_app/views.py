from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'admin_app/admindashboard.html')  # Render the admin dashboard

def bookings(request):
    return render(request, 'admin_app/adminbookings.html')    # Render the bookings page

def statistics(request):
    return render(request, 'admin_app/adminstatistics.html')   # Render the statistics page

def login(request):
    return render(request, 'admin_app/adminlogin.html')
