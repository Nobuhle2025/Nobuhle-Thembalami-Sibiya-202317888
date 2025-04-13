from django import forms
from .models import ClassSchedule # type: ignore
from .models import MoodEntry
from .models import Assignment



class ClassScheduleForm(forms.ModelForm):
    class Meta:
        model = ClassSchedule
        fields = ['class_name', 'class_day', 'class_time_start', 'class_time_end', 'location']
        widgets = {
            'class_day': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'class_time_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'class_time_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'class_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import ClassSchedule # type: ignore

class ClassScheduleForm(forms.ModelForm):
    class Meta:
        model = ClassSchedule
        fields = ['class_name', 'class_day', 'class_time_start', 'class_time_end', 'location']



class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['mood', 'thoughts']



        

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'course', 'due_date']