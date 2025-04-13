from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.models import User 
from .models import Assignment, ClassSchedule
from django.contrib.auth.decorators import login_required
from .forms import ClassScheduleForm # type: ignore
from .forms import MoodEntryForm
from .models import MoodEntry
from django.contrib import messages
import json
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import MoodCheckIn





def dashboard(request):
    assignments = Assignment.objects.filter(user=request.user)
    schedule = ClassSchedule.objects.filter(user=request.user)
    
    return render(request, 'core/dashboard.html', {
        'assignments': assignments,
        'schedule': schedule,
       
    })



def home(request):

    return render(request, 'core/home.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')  

        user = authenticate(request, username=username, password=password)

        if user is not None:
         
            login(request, user)
            return redirect('dashboard')  
        else:
          
            messages.error(request, "Invalid username or password")
            return redirect('login')  

    return render(request, 'core/home.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

       
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

       
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')

        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

      
        user = User.objects.create_user(username=username, email=email, password=password)

        print("User successfully created!")
        login(request, user)

        return redirect('home')

    return render(request, 'core/register.html')



def logout_view(request):
    logout(request)
    return redirect('login')


def assignments_view(request):
    return render(request, 'core/assignments.html')

def add_assignment_view(request):
    # Logic for adding an assignment
    return render(request, 'core/add_assignment.html')






from .models import ClassSchedule


def schedule_view(request):
    schedules = ClassSchedule.objects.filter(user=request.user)  

    if request.method == "POST":
        form = ClassScheduleForm(request.POST)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.user = request.user  
            new_class.save()
            return redirect('schedule')  

    else:
        form = ClassScheduleForm()

    return render(request, 'core/schedule.html', {'form': form, 'schedules': schedules})





def wellness_view(request):
    if request.method == 'POST':
        mood = request.POST.get('mood')
        thoughts = request.POST.get('thoughts')
       
        messages.success(request, 'Your wellness check-in has been submitted.')
        return redirect('wellness')  
    return render(request, 'core/wellness.html')




@login_required
def add_class(request):
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST)
        if form.is_valid():
            class_schedule = form.save(commit=False)
            class_schedule.user = request.user
            class_schedule.save()
            return redirect('schedule')
    else:
        form = ClassScheduleForm()
    return render(request, 'add_class.html', {'form': form})


import json

def wellness_checkin(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood_entry = form.save(commit=False)
            mood_entry.user = request.user
            mood_entry.save()
            messages.success(request, 'Your mood has been logged!')
            return redirect('wellness')
    else:
        form = MoodEntryForm()

    mood_data = MoodEntry.objects.filter(user=request.user)
    calendar_data = [
        {"date": entry.date.strftime("%Y-%m-%d"), "mood": entry.mood}
        for entry in mood_data
    ]

    return render(request, 'wellness.html', {
        'form': form,
        'calendar_data': json.dumps(calendar_data)
    })






def calendar_view(request):
    assignments = Assignment.objects.filter(user=request.user)
    
 
    assignments_json = json.loads(serialize('json', assignments, 
        fields=('title', 'due_date'),
        use_natural_foreign_keys=True))
    
   
    events = [{
        'title': item['fields']['title'],
        'start': item['fields']['due_date'],
        'color': '#007bff'
    } for item in assignments_json]
    
    return render(request, 'calendar.html', {
        'assignments_json': json.dumps(events)
    })

def assignment_api(request):
    if not request.user.is_authenticated:
        return JsonResponse([], safe=False)
    
    assignments = Assignment.objects.filter(user=request.user)
    data = [{
        'title': a.title,
        'start': a.due_date.isoformat(),
        'color': '#28a745' if a.completed else '#dc3545'
    } for a in assignments]
    
    return JsonResponse(data, safe=False)  



def mood_chart(request):
    mood_entries = MoodCheckIn.objects.filter(user=request.user).order_by('date')

    date_data = [entry.date.strftime('%Y-%m-%d') for entry in mood_entries]
    mood_data = [entry.mood_value for entry in mood_entries]
    productivity_data = [entry.productivity_score for entry in mood_entries]

    context = {
        'date_data': json.dumps(date_data),
        'mood_data': json.dumps(mood_data),
        'productivity_data': json.dumps(productivity_data),
    }

    return render(request, 'core/mood_chart.html', context)