# pylint: disable=missing-module-docstring

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class RecurrenceRate(models.IntegerChoices): # pylint: disable=missing-class-docstring
    NEVER = -1, _('Never')
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
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    # TODO: This code contains a few major flaws.
    # 1. A circular dependency between projects is possible. This should be fine if I'm not using a tree structure at all.
    # 2. A projects and the sub projects can end up with different users. Normally this shouldn't happen because the
    #    views will handle that part but it's possible nonetheless and can be a major headache that should be resolved
    #    within models if possible.

    def __str__(self): # pylint: disable=invalid-str-returned
        return self.name

class Task(models.Model): # pylint: disable=missing-class-docstring
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField()
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    due_time = models.TimeField(null=True)
    recurrence = models.IntegerField(choices=RecurrenceRate)

    # TODO: This code contains a few major flaws.
    # 1. A tasks can have a different user than the project if there's one.
    # 2. Recurrence rate being Never is handled here using a custom value unlike before when Null was used but wasn't working.
    #    I don't know the consequences of this.

    def __str__(self): # pylint: disable=invalid-str-returned
        return self.name

class TaskInstance(models.Model): # pylint: disable=missing-class-docstring
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # TODO: In admin portal, this must be the same as tasks model, or alternatively, all since almost no operations here
    # should be done by admins, it should appear as read only fields for sorting and filtering.

    class Meta: # pylint: disable=missing-class-docstring
        db_table = 'core_task_instance'
