from django.contrib import admin
from django.urls import path
from .views import HomeView, CreateYearGoalView, FeedbackView


# 名前空間を設定
app_name = "goal"

urlpatterns = [
    path("year_goal/", CreateYearGoalView.as_view(), name="year_goal"),
    path("", HomeView.as_view(), name="home"),
    path("feedback/", FeedbackView.as_view(), name="feedback"),
]
