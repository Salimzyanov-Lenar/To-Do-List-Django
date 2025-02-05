from django.forms import ModelForm, DateInput
from .models import Task


class TaskForm(ModelForm):
    """ Форма для создания заметки """
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'deadline']
        widgets = {
            'deadline': DateInput(attrs={'type': 'date'})
        }

    def save(self, commit=True, user=None):
        task = super().save(commit=False)
        if user:
            task.user = user
        if commit:
            task.save()
        return task