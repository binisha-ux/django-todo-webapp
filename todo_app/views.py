from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "index.html") 

def register_view(request):
    if request.method == "POST":
        data = request.POST

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        username= data.get('username')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )
        return redirect('login')

        
    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        data = request.POST

        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, "Invalid credentials. ")           
            return redirect('login')

    return render(request, "login.html")

def logout_view(request):
    return render(request, "logout.html")

def delete_task(request, id):
    return HttpResponse("deleted")