from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Status(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(
                    max_length=32, 
                    help_text='Title for the task')

    description = models.CharField(
                    max_length=256,
                    blank=True, default='', 
                    help_text='A longer description for the task (optional)')

    status = models.ForeignKey(
                    Status, 
                    on_delete=models.RESTRICT, 
                    help_text='The task status')

    due_date = models.DateTimeField(
                    help_text='When the task is due')

    user = models.ForeignKey(User, 
                            models.SET_NULL,
                            blank=True,
                            null=True)

    @property
    def due_date_in_the_past(self):
        return self.due_date <= timezone.now()

    def __str__(self):
        return self.title