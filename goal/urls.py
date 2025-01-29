from django.contrib import admin
from django.urls import path
from .views import HomeView

# 名前空間を設定
app_name = 'goal'

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
