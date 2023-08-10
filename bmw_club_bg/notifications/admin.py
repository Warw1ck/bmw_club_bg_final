from django.contrib import admin

# Register your models here.
from bmw_club_bg.notifications.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    # List of fields to display in the list view
    list_display = ('user', 'user_like', 'content', 'timestamp', 'is_read')

    # Fields to use for filtering in the right sidebar
    list_filter = ('is_read', 'timestamp', 'user')

    # Fields to search for in the search bar
    search_fields = ('content',)

    # Enable date-based navigation in the top bar
    date_hierarchy = 'timestamp'


admin.site.register(Notification, NotificationAdmin)