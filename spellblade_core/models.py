from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=25)

    class Meta:
        db_table = 'core_project'

        constraints = [
            models.UniqueConstraint(fields=('user', 'name'), name='unique_project_name'),
        ]

    def __str__(self):
        return self.name

class Section(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=25)

    class Meta:
        db_table = 'core_section'

        constraints = [
            models.UniqueConstraint(fields=('project', 'name'), name='unique_section_name'),
        ]

    def __str__(self):
        return self.name

class RecurringFrequency(models.IntegerChoices):
    NEVER = -1, _('Never')
    EVERY_DAY = 0, _('Every day')
    EVERY_WEEK = 1, _('Every week')

class Task(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    due_at = models.DateTimeField(_('due date'), null=True, blank=True)
    recurrence = models.IntegerField(_('recurring frequency'), choices=RecurringFrequency.choices, default=RecurringFrequency.NEVER)

    class Meta:
        db_table = 'core_task'

        constraints = [
            models.UniqueConstraint(fields=('section', 'name'), name='unique_task_name'),
            models.CheckConstraint(
                check=models.Q(recurrence=RecurringFrequency.NEVER) | models.Q(due_at__isnull=False),
                name='task_recurrence_requires_due_date',
                violation_error_message=_('The due date must be set if the task is recurring.'),
            ),
        ]

    def __str__(self):
        return self.name
