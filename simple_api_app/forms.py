from django import forms
from django.forms import fields
from .models import Task
from formset.widgets import DateTimeInput

class TaskForm(forms.ModelForm):

    due_date = fields.DateTimeField(
        widget=DateTimeInput
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'