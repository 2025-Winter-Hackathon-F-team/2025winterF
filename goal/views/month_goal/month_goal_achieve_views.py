import logging
import json

from django.views.generic import UpdateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from goal.models.month_goal import MonthGoal
from goal.models.todo import Todos

logger = logging.getLogger(__name__)

class MonthGoalAchieveView(LoginRequiredMixin, UpdateView):
    model = MonthGoal

    def get_object(self, month_goal_id):
        """
        更新対象の月の目標を取得する
        Returns:
            MonthGoal: 指定された月の目標が存在すれば MonthGoal インスタンスを返す
        """

        # 指定された月の目標を取得
        month_goal = MonthGoal.get_month_goal(month_goal_id=month_goal_id)
        if not month_goal:
            logger.warning(f"[MonthGoal] Not found: month_id={month_goal_id}")
            return None

        return month_goal

    def post(self, request, *args, **kwargs):
        """
        月目標を達成状態に更新するAPIエンドポイント
        Args:
            request (HttpRequest): クライアントからのリクエスト
        Returns:
            JsonResponse:
                - 成功時: 更新処理が完了したことを返す (status=200)
                - 失敗時: エラーメッセージを返す (status=400, 404, 500)
        """
        try:
            # リクエストボディをJSONとして読み込む
            data = json.loads(request.body)
        except json.JSONDecodeError:
            logger.warning("[MonthGoalAchieveView] Invalid JSON format in request body")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        month_goal_id = data.get("month_id")
        if month_goal_id is None:
            logger.warning("[MonthGoalAchieveView] month_id is missing in request data")
            return JsonResponse({"error": "month_id is required"}, status=400)

        month_goal = self.get_object(month_goal_id)
        if not month_goal:
            return JsonResponse({"error": "MonthGoal not found."}, status=404)

        try:
            # 月目標を達成状態にする
            month_goal.mark_as_achieved()
            logger.info(f"[MonthGoal] Marked month_goal {month_goal.id} as achieved.")
        except Exception as e:
            logger.error(f"[MonthGoal] Error marking month_goal {month_goal.id} as achieved: {e}")
            return JsonResponse({"error": "Failed to mark month goal as achieved."}, status=500)

        # 未達成のTodoを達成済みに更新
        update_todo_count = Todos.mark_as_achieved_for_goal(month_goal=month_goal)
        if update_todo_count > 0:
            logger.info(f"[Todos] Updated {update_todo_count} todos as achieved for month_goal={month_goal.id}")
        else:
            logger.info(f"[Todos] No todos were updated for month_goal={month_goal.id}")

        return JsonResponse({"success": "Successfully processed request"}, status=200)