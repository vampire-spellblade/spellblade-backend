from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_user_master = models.BooleanField(default=False) # Each user must have exactly one master project.

    def __str__(self):
        return self.name

class Section(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.TextField()
    is_project_master = models.BooleanField(default=False) # Each project must have exactly one master section.

    def __str__(self):
        return self.name

class RecurrenceRate(models.IntegerChoices):
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
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField(blank=True)
    due_at = models.DateTimeField(null=True, blank=True)
    recurrence_rate = models.IntegerField(choices=RecurrenceRate.choices, default=RecurrenceRate.NEVER)
    sub_tasks_complete = models.IntegerField(default=0)
    sub_tasks_total = models.IntegerField(default=0)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

# TODO: Implement priority/difficulty system. (Priority: High)
# TODO: Implement team/guild system. (Priority: Low)
# TODO: Determine how to allow users to order projects, sections, and tasks in the way they like. (Priority: Medium)
