# pylint: disable=missing-module-docstring

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class RecurrenceRate(models.IntegerChoices): # pylint: disable=missing-class-docstring
    EVERY_DAY = 0, _('Every Day')
    EVERY_SUNDAY = 1, _('Every Sunday')
    EVERY_MONDAY = 2, _('Every Monday')
    EVERY_TUESDAY = 3, _('Every Tuesday')
    EVERY_WEDNESDAY = 4, _('Every Wednesday')
    EVERY_THURSDAY = 5, _('Every Thursday')
    EVERY_FRIDAY = 6, _('Every Friday')
    EVERY_SATURDAY = 7, _('Every Saturday')

class Project(models.Model): # pylint: disable=missing-class-docstring
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField()
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self): # pylint: disable=invalid-str-returned
        return self.name

class Task(models.Model): # pylint: disable=missing-class-docstring
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField()
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    due_time = models.TimeField(null=True)
    recurrence = models.IntegerField(choices=RecurrenceRate, null=True)

    def __str__(self): # pylint: disable=invalid-str-returned
        return self.name

class TaskInstance(models.Model): # pylint: disable=missing-class-docstring
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    due_date = models.DateField(null=True)
    completed_at = models.DateTimeField(null=True)

    class Meta: # pylint: disable=missing-class-docstring
        db_table = 'core_task_instance'
