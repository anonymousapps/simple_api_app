from django.db import models

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
                    help_text='A longer description for the task')

    status = models.ForeignKey(
                    Status, 
                    on_delete=models.RESTRICT, 
                    help_text='The task status')

    due_date = models.DateTimeField(
                    'Due date/time', 
                    help_text='When the task is due')

    def __str__(self):
        return self.title