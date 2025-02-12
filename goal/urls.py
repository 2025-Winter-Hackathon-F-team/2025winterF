from django.urls import path

from .views import HomeView, CreateYearGoalView, YearGoalDetailView, YearGoalUpdateView, FeedbackView


# 名前空間を設定
app_name = "goal"

urlpatterns = [
    path("year_goal/create/", CreateYearGoalView.as_view(), name="create_year_goal"),
    # 年指定なしでアクセス（今年の目標）
    path("year_goal/detail/", YearGoalDetailView.as_view(), name="year_goal_detail"),
    # 年を指定した場合
    path("year_goal/detail/<int:year>/", YearGoalDetailView.as_view(), name="year_goal_detail_year"),
    # 年目標のタイトルを更新
    path("year_goal/<int:year>/edit/", YearGoalUpdateView.as_view(), name="year_goal_edit"),
    path("", HomeView.as_view(), name="home"),
    path("feedback/", FeedbackView.as_view(), name="feedback"),
]
