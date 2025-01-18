from django.urls import path
from .views import hello_world, hello_mysql


urlpatterns = [
    path('', hello_world),
    path('mysql/', hello_mysql)
]