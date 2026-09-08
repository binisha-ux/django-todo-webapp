from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Task
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='login')
def dashboard(request):
    if request.method == "POST":
        data = request.POST

        title = data.get('title')
        description = data.get('description')
        due_date = data.get('due_date')
        priority = request.POST.get('priority', 'Low')

        if title and due_date:
            Task.objects.create(
                user=request.user,
                title=title,
                description = description,
                due_date=due_date,
                priority=priority
            )
            return redirect('dashboard')

    tasks = Task.objects.filter(user=request.user).order_by('-due_date')

    context = {'tasks':tasks}



    return render(request, "dashboard.html", context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

@login_required(login_url='login')
def update_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    if request.method == "POST":
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.due_date = request.POST.get('due_date')
        task.priority = request.POST.get('priority', 'Low')
        task.save()
        return redirect('dashboard')  # Use the URL route name here

    formatted_date = task.due_date.strftime('%Y-%m-%d') if task.due_date else ''

    context = {
        'task': task,
        'formatted_date': formatted_date
    }

    return render(request, "update.html", context)

@login_required(login_url='login')
def logout_view(request):
    return render(request, "logout.html")


@login_required(login_url='login')
def delete_task(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.delete()
    return redirect("dashboard")