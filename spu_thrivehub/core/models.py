from django.db import models
from django.contrib.auth.models import User



class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ClassSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='class_schedules')
    class_name = models.CharField(max_length=100)
    class_day = models.CharField(max_length=20)
    class_time_start = models.TimeField()
    class_time_end = models.TimeField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.class_name} on {self.class_day}"
    

class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ('Happy', 'Happy'),
        ('Sad', 'Sad'),
        ('Stressed', 'Stressed'),
        ('Relaxed', 'Relaxed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    thoughts = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood} on {self.date}"






from django.contrib.auth.models import User

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 👈 Add this line
    title = models.CharField(max_length=100)
    description = models.TextField()
    course = models.CharField(max_length=100, blank=True)
    due_date = models.DateField()

def __str__(self):
    return self.title


class MoodCheckIn(models.Model):
    MOOD_CHOICES = [
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Neutral'),
        (4, 'Good'),
        (5, 'Very Good'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    mood = models.IntegerField(choices=MOOD_CHOICES)
    productivity = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.date} - Mood: {self.mood}"