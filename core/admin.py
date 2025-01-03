# pylint: disable=missing-module-docstring
from django.contrib import admin
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin): # pylint: disable=missing-class-docstring
    ordering = ('user', 'name',)
    list_display = ('user', 'name',)
    search_fields = ('user', 'name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin): # pylint: disable=missing-class-docstring
    ordering = ('project', 'name',)
    list_display = ('project', 'name', 'due', 'recurrence_rate',)
    search_fields = ('project', 'name',)
