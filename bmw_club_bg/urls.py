from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('bmw_club_bg.common.urls')),
    path('authentication/', include('bmw_club_bg.accounts.urls')),
    path('groups/', include('bmw_club_bg.groups.urls')),
    path('profile/', include('bmw_club_bg.profiles.urls')),
    path('notifications/', include('bmw_club_bg.notifications.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
