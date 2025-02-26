from django.urls import path

from .views import (
    HomeView,
    CreateYearGoalView,
    YearGoalDetailView,
    YearGoalUpdateView,
    YearGoalAchievementView,
    MontGoalDetailView,
    MonthGoalAchieveView,
    MonthGoalUpdateView,
    TodoCreateView,
    TodoDetailView,
    TodoUpdateView,
    TodoAchieveView,
    UnachievedTodoCheckView,
    FeedbackView,
    FeedbackGoodView,
)


# 名前空間を設定
app_name = "goal"

urlpatterns = [
    path("year_goal/create/", CreateYearGoalView.as_view(), name="create_year_goal"),
    # 年指定なしでアクセス（今年の目標）
    path("year_goal/detail/", YearGoalDetailView.as_view(), name="year_goal_detail"),
    # 年を指定した場合
    path(
        "year_goal/detail/<int:year>/",
        YearGoalDetailView.as_view(),
        name="year_goal_detail_year",
    ),
    # 年目標のタイトルを更新
    path(
        "year_goal/<int:year>/edit/",
        YearGoalUpdateView.as_view(),
        name="year_goal_edit",
    ),
    path(
        "year_goal/<int:year>/achieve/",
        YearGoalAchievementView.as_view(),
        name="year_goal_achieve",
    ),
    path(
        "year_goal/<int:year>/has_unachieved_goals/",
        YearGoalAchievementView.as_view(),
        name="year_goal_achievement",
    ),
    path(
        "year_goal/<int:year_goal_id>/achieve_only_year/",
        YearGoalAchievementView.as_view(),
        name="year_goal_achieve_only_year",
    ),
    # 年指定なしでアクセス（月の目標）
    path(
        "year_goal/month_goal/<int:month>/",
        MontGoalDetailView.as_view(),
        name="month_goal_detail",
    ),
    # 年を指定した場合（月の目標）
    path(
        "year_goal/<int:year>/month_goal/<int:month>/",
        MontGoalDetailView.as_view(),
        name="month_goal_detail_specific_year",
    ),
    path(
        "year_goal/month_goal/<int:year>/<int:month>/edit/",
        MonthGoalUpdateView.as_view(),
        name="month_goal_edit",
    ),
    # Todo作成画面（年指定なし）
    path(
        "year_goal/month_goal/<int:month>/todo/create/",
        TodoCreateView.as_view(),
        name="create_todo",
    ),
    # Todo作成画面（年指定あり）
    path(
        "year_goal/<int:year>/month_goal/<int:month>/todo/create/",
        TodoCreateView.as_view(),
        name="create_todo_specific_year",
    ),
    # 月目標の状態を達成に変更する
    path(
        "year_goal/<int:year>/month_goal/<int:month>/achieve/",
        MonthGoalAchieveView.as_view(),
        name="month_goal_achieve",
    ),
    # 月目標に紐づく未達成のTodoがあるか確認
    path(
        "year_goal/<int:year>/month_goal/<int:month>/has_unachieved_todos/",
        UnachievedTodoCheckView.as_view(),
        name="has_unachieved_todos",
    ),
    # Todo詳細画面（年指定なし）
    path(
        "year_goal/month_goal/<int:month>/todo/<int:todo>",
        TodoDetailView.as_view(),
        name="todo_detail",
    ),
    # Todo詳細画面（年指定あり）
    path(
        "year_goal/<int:year>/month_goal/<int:month>/todo/<int:todo>",
        TodoDetailView.as_view(),
        name="todo_detail_specific_year",
    ),
    # ToToのタイトルを更新(年指定なし)
    path(
        "year_goal/month_goal/<int:month>/todo/<int:todo>/update/",
        TodoUpdateView.as_view(),
        name="todo_update",
    ),
    # ToToのタイトルを更新(年指定あり)
    path(
        "year_goal/<int:year>/month_goal/<int:month>/todo/<int:todo>/update/",
        TodoUpdateView.as_view(),
        name="todo_update_specific_year",
    ),
    # Todoの状態を達成に変更する
    path(
        "year_goal/<int:year>/month_goal/<int:month>/todo/<int:todo>/achieve/",
        TodoAchieveView.as_view(),
        name="todo_achieve",
    ),
    path("", HomeView.as_view(), name="home"),
    # フィードバック画面（bad_message）
    path("feedback/", FeedbackView.as_view(), name="feedback"),
    # フィードバック画面（good_message）
    path("feedback_good/", FeedbackGoodView.as_view(), name="feedback_good"),
]
