from django.contrib import admin
from bmw_club_bg.common.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    # List of fields to display in the list view
    list_display = ('content', 'author', 'date')

    # Fields to use for filtering in the right sidebar
    list_filter = ('author', 'date')

    # Fields to search for in the search bar
    search_fields = ('content',)

    # Enable date-based navigation in the top bar
    date_hierarchy = 'date'


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    list_filter = ('timestamp', 'user')
    search_fields = ('post', 'user')
    date_hierarchy = 'timestamp'


admin.site.register(Comment, CommentAdmin)