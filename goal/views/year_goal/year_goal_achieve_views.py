from datetime import date
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from goal.models import MonthGoal, Todos, YearGoal
from account.models import User

logger = logging.getLogger(__name__)


class YearGoalAchievementView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """
        指定されたユーザーに関連する未完了の年目標、月目標、ToDoが存在するかどうかを返す。
        """
        year = self.kwargs.get("year")
        user = self.request.user

        # 年目標取得
        year_start_date = date(year, 1, 1)
        year_goal = YearGoal.get_year_goal_for_user(user=user, year=year_start_date)

        # 年目標に紐づく月目標を取得
        month_goals = MonthGoal.objects.filter(year_goal=year_goal).order_by("month")
        # 月目標とTodoに未達成があるか確認
        for month_goal in month_goals:
            if (month_goal.status == MonthGoal.STATUS_UNACHIEVED) or (
                Todos.has_unachieved(month_goal)
            ):
                return JsonResponse({"has_unachieved": True})

        # 月,todoに未達成がない場合
        return JsonResponse({"has_unachieved": False})

    def post(self, request, year_goal_id):
        """
        指定された年目標を達成済みに更新する。
        """
        try:
            with transaction.atomic():
                year_goal = get_object_or_404(
                    YearGoal, id=year_goal_id, user=request.user
                )
                year_goal.status = YearGoal.STATUS_ACHIEVED
                year_goal.save()
                return JsonResponse(
                    {"success": "Year goal marked as achieved."},
                    status=200,
                )
        except YearGoal.DoesNotExist:
            logger.warning(
                f"YearGoal not found for user {request.user.id}: {year_goal_id}"
            )
            return JsonResponse(
                {"error": "指定された年目標が見つかりませんでした。"}, status=404
            )
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while achieving YearGoal {year_goal_id} for user {request.user.id}: {e}",
                exc_info=True,
            )
            return JsonResponse(
                {"error": "目標の達成処理中にエラーが発生しました。"}, status=500
            )
