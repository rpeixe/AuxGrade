from django.shortcuts import render

# Create your views here.
def login_screen(request):
    return render(request,"login.html")