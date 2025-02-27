from datetime import date
import logging
import json

from django.http import JsonResponse
from django.views import View

from goal.models.month_goal import MonthGoal
from goal.models.todo import Todos
from goal.models.year_goal import YearGoal

logger = logging.getLogger(__name__)


class UnachievedTodoCheckView(View):

    def get_object(self, year, month):
        """
        更新対象の月の目標を取得する
        Returns:
            MonthGoal: 指定された月の目標が存在すれば MonthGoal インスタンスを返す
        """
        user = self.request.user
        # 年をdatetime.dateに変換
        year_start_date = date(year, 1, 1)
        year_goal = YearGoal.get_year_goal_for_user(user=user, year=year_start_date)
        if not year_goal:
            logger.warning(
                f"[YearGoal] Not found: user={user.id}, year={year_start_date}."
            )
            return None

        month_goal = MonthGoal.get_specific_month_goal(year_goal=year_goal, month=month)
        if not month_goal:
            logger.warning(
                f"[MonthGoal] Not found: month={month}, year_goal={year_goal.id}"
            )
            return month_goal

        return month_goal

    def get(self, request, *args, **kwargs):
        """
        指定された年月の月目標に関連する未達成のTodoがあるかをJSONで返す
        Args:
            request (HttpRequest): クライアントからのGETリクエスト
        Returns:
            JsonResponse:
                - 未達成のTodoがある場合: {"has_unachieved_todos": true}
                - 未達成のTodoがない場合: {"has_unachieved_todos": false}
                - 指定された月目標のTodoが存在しない場合: エラーメッセージ (status=404)
                - 予期せぬエラーが発生した場合: エラーメッセージ (status=500)
        """
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        try:
            month_goal = self.get_object(year, month)
            has_unachieved = Todos.has_unachieved(month_goal=month_goal)
            if has_unachieved is None:
                # Todoが存在しない場合のエラーハンドリング
                logger.warning(
                    f"[Todo] Not found for month_goal={month_goal.id} in year {year}, month {month}."
                )
                return JsonResponse(
                    {"error": "Todo not found for the specified month goal."},
                    status=404,
                )
            return JsonResponse({"has_unachieved_todos": has_unachieved})
        except Exception as e:
            # 一般的な例外のキャッチ
            logger.exception(f"Unexpected error: {str(e)}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)
