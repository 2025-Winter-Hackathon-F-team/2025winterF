import datetime
import logging
import json

from django.views.generic import UpdateView
from django.http import JsonResponse, Http404
from goal.models import MonthGoal, YearGoal
from django.core.exceptions import ValidationError, PermissionDenied

logger = logging.getLogger(__name__)


class MonthGoalUpdateView(UpdateView):
    model = MonthGoal

    def get_object(self, queryset=None):
        """
        更新対象の月目標を取得する
        """
        try:
            year = int(self.kwargs.get("year"))
            month = int(self.kwargs.get("month"))
        except (TypeError, ValueError) as e:
            logger.warning(
                f"Invalid year or month parameter: year={self.kwargs.get('year')}, month={self.kwargs.get('month')}"
            )
            raise Http404("Invalid year or month parameter")

        # year を "2025-01-01" の形式に変換
        year_str = f"{year}-01-01"

        # YearGoalインスタンス取得
        year_goal = YearGoal.get_year_goal_for_user(self.request.user, year_str)
        if not year_goal:
            logger.warning(
                f"[YearGoal] Not found: user_id={self.request.user.id}, year={year_str}"
            )
            raise Http404("Year goal not found")
        # YearGoalID取得
        year_goal_id = year_goal.id

        # MonthGoalインスタンス取得
        month_goal = MonthGoal.get_specific_month_goal(year_goal_id, month)
        if not month_goal:
            logger.warning(
                f"[MonthGoal] Not found: user_id={self.request.user.id}, year={year}, month={month}"
            )
            raise Http404("Month goal not found")

        # 権限チェック（念のため）
        if month_goal.year_goal.user != self.request.user:
            logger.warning(
                f"Unauthorized access attempt by user_id={self.request.user.id} to month_goal_id={month_goal.id}"
            )
            raise PermissionDenied("You do not have permission to edit this goal.")

        return month_goal

    def post(self, request, *args, **kwargs):
        """
        月目標のタイトルを更新するためのAPIエンドポイント
        """
        # 月目標を取得
        month_goal = self.get_object()

        # リクエストボディからデータを取得
        try:
            data = json.loads(request.body)
            logger.info(f"Received data: {data}")

            new_title = data.get("title", "").strip()
            if not new_title:
                logger.warning("Title is missing or empty.")
                return JsonResponse(
                    {"error": {"title": ["タイトルを入力してください。"]}}, status=400
                )
        except json.JSONDecodeError:
            logger.warning("Invalid JSON format in request body.")
            return JsonResponse(
                {"error": {"title": ["無効なデータ形式です。"]}}, status=400
            )

        # タイトルを更新
        try:
            month_goal.update_title(new_title)
            logger.info("Title update successful.")
            return JsonResponse({"title": month_goal.title}, status=200)
        except ValidationError as e:
            logger.warning(f"Validation error updating MonthGoal: {e}")
            return JsonResponse({"error": e.message_dict}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error updating MonthGoal: {e}")
            return JsonResponse(
                {"error": {"title": ["保存に失敗しました。"]}}, status=500
            )
