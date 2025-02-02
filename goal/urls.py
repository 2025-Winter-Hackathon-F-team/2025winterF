from django.contrib import admin
from django.urls import path
from .views import HomeView
from .views import CreateYearGoalView

# 名前空間を設定
app_name = 'goal'

urlpatterns = [
    path('create/', CreateYearGoalView.as_view(), name='create'),
    path("", HomeView.as_view(), name="home"),
]
