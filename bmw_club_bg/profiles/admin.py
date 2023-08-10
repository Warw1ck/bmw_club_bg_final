from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'birthday', 'gender')
    list_filter = ('gender',)
    search_fields = ('user__username', 'first_name', 'last_name')
    date_hierarchy = 'birthday'


admin.site.register(Profile, ProfileAdmin)

