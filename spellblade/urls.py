'''URL configuration for spellblade project.'''
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
