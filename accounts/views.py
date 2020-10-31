from django.shortcuts import redirect,render
from django.contrib.auth import login, authenticate, logout
from .models import Account
from django.contrib import messages

# Create your views here.
def signup_user(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=Account.objects.create_user(email=email,password=password)
            messages.success(request, 'Profile Created')
            return redirect("accounts:login")

        except :
            messages.error(request,'Username already exists! Try another one')
            return redirect("accounts:signup")

    return render(request,'signup.html')

def login_user(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            return redirect("frontend:home")
        else:
            messages.error(request,'Incorrect username/password')
            return redirect("accounts:login")

    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return render(request,"login.html")

