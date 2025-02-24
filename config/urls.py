from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/tasks/', permanent=False)),

    # Apps
    path('tasks/', include('tasks.urls')),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'tasks.views.custom_page_not_found_view'