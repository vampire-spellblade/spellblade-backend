from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# TODO: Update these models. (Priority: High)

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'name',)

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
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_at = models.DateTimeField()
    recurrence_rate = models.IntegerField(choices=RecurrenceRate.choices, default=RecurrenceRate.NEVER)

    def __str__(self):
        return self.name
