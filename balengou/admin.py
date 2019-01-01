from django.contrib import admin
from balengou.models import *
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','team')
    search_fields = ('name',)
    list_filter = ('team',)


class ProjectInline(admin.TabularInline):
    model = Project


class TeamAdmin(admin.ModelAdmin):
    inlines = (ProjectInline,)

admin.site.register(Team, TeamAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(ProductBacklog)
admin.site.register(Sprint)
admin.site.register(UserStory)