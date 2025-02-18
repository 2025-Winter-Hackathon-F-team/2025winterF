from django.urls import path

from .views import HomeView, CreateYearGoalView, YearGoalDetailView, YearGoalUpdateView, MontGoalDetailView, MonthGoalCompleteView, TodoCreateView, UnachievedTodoCheckView, FeedbackView


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
    # 年指定なしでアクセス（月の目標）
    path("year_goal/month_goal/<int:month>/", MontGoalDetailView.as_view(), name="month_goal_detail"),
    # 年を指定した場合（月の目標）
    path("year_goal/<int:year>/month_goal/<int:month>/", MontGoalDetailView.as_view(), name="month_goal_detail_specific_year"),
    # Todo作成画面（年指定なし）
    path("year_goal/month_goal/<int:month>/todo/create/", TodoCreateView.as_view(), name="create_todo"),
    # Todo作成画面（年指定あり）
    path("year_goal/<int:year>/month_goal/<int:month>/todo/create/", TodoCreateView.as_view(), name="create_todo_specific_year"),
    # 月目標の状態を達成に変更する
    path("year_goal/<int:year>/month_goal/<int:month>/complete/", MonthGoalCompleteView.as_view(), name="month_goal_complete"),
    # 月目標に紐づく未達成のTodoがあるか確認
    path("year_goal/<int:year>/month_goal/<int:month>/has_unachieved_todos/", UnachievedTodoCheckView.as_view(), name="has_unachieved_todos"),
    path("", HomeView.as_view(), name="home"),
    path("feedback/", FeedbackView.as_view(), name="feedback"),
]
