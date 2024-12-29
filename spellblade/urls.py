# pylint: disable=missing-module-docstring

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls')),
]
