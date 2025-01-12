from django.contrib import admin
from .models import Project, Section, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',)
    search_fields = ('user__username', 'name',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'user',)
    search_fields = ('project__user__username', 'project__name', 'name',)

    def user(self, obj):
        return obj.project.user

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'project', 'user', 'due_at', 'recurrence',)
    search_fields = ('section__project__user__username', 'section__project__name', 'section__name', 'name',)

    def project(self, obj):
        return obj.section.project

    def user(self, obj):
        return obj.section.project.user
