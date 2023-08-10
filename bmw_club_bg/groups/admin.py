from django.contrib import admin

from bmw_club_bg.groups.models import Group


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_creation', 'created_by')
    list_filter = ('date_of_creation',)
    search_fields = ('name', 'created_by')
    date_hierarchy = 'date_of_creation'


admin.site.register(Group, GroupAdmin)
