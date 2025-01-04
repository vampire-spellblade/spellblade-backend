# pylint: disable=missing-module-docstring
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    '''Project model for task management.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        unique_together = ('user', 'name',)

    def __str__(self): # pylint: disable=invalid-str-returned
        return self.name

class RecurrenceRate(models.IntegerChoices):
    '''RecurrenceRate enum to manage task recurrence.'''
    NEVER = -1, 'Never'
    EVERY_DAY = 0, 'Every day'
    EVERY_SUNDAY = 1, 'Every Sunday'
    EVERY_MONDAY = 2, 'Every Monday'
    EVERY_TUESDAY = 3, 'Every Tuesday'
    EVERY_WEDNESDAY = 4, 'Every Wednesday'
    EVERY_THURSDAY = 5, 'Every Thursday'
    EVERY_FRIDAY = 6, 'Every Friday'
    EVERY_SATURDAY = 7, 'Every Saturday'

class Task(models.Model):
    '''Task model for task management.'''
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    recurrence_rate = \
        models.IntegerField(choices=RecurrenceRate.choices, default=RecurrenceRate.NEVER)

    def __str__(self): # pylint: disable=invalid-str-returned
        return self.name
