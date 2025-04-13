from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('assignments/', views.assignments_view, name='assignments'),
    path('assignments/add/', views.add_assignment_view, name='add_assignment'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('wellness/', views.wellness_view, name='wellness'),
    path('schedule/add/', views.add_class, name='add_class'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('mood_chart/', views.mood_chart, name='mood_chart'),
]
