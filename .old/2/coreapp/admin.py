from django.contrib import admin
from .models import Project, Section, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    ordering = ('user__username', 'name',)
    list_display = ('name', 'user__username', 'is_user_master',)
    search_fields = ('user__username', 'name',)
    list_filter = ('is_user_master',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    ordering = ('project__user__username', 'project__name', 'name',)
    list_display = ('name', 'project__name', 'project__user__username', 'is_project_master',)
    search_fields = ('project__user__username', 'project__name', 'name',)
    list_filter = ('is_project_master',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    ordering = ('section__project__user__username', 'section__project__name', 'section__name', 'name',)
    list_display = ('name', 'section__name', 'section__project__name', 'section__project__user__username', 'due_at', 'recurrence_rate', 'sub_tasks_complete', 'sub_tasks_total',)
    search_fields = ('section__project__user__username', 'section__project__name', 'section__name', 'name',)
