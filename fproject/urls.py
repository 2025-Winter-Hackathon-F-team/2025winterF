from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', include('fapp.urls')),
    path('fapp/', include('fapp.urls')),
]
