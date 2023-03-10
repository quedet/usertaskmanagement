from django import forms
from apps.tasks.models import Task


class CustomDate(forms.widgets.DateInput):
    template_name = 'form/flatpickr_date.html'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        widgets = {
            'due_date': CustomDate()
        }
