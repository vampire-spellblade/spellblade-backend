from django.contrib import admin
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    ordering = ('user', 'name',)
    list_display = ('name', 'user',)
    search_fields = ('user__username', 'name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    ordering = ('project', 'name',)
    list_display = ('name', 'project', 'due_at', 'recurrence_rate',)
    search_fields = ('project__name', 'name',)
