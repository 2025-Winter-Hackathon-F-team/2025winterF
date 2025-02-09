from django.urls import path
from .views import HomeView, CreateYearGoalView

# 名前空間を設定
app_name = "goal"

urlpatterns = [
    path("year_goal/create/", CreateYearGoalView.as_view(), name="create_year_goal"),
    path("", HomeView.as_view(), name="home"),
]
