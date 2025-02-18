import logging
import json

from django.views.generic import UpdateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from goal.models.month_goal import MonthGoal

logger = logging.getLogger(__name__)

class MonthGoalCompleteView(LoginRequiredMixin, UpdateView):
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
            return month_goal

        return month_goal

    def post(self, request, *args, **kwargs):
        # リクエストボディをJSONとして読み込む
        data = json.loads(request.body)
        logger.info(f"Received data: {data}")
        month_goal_id = data.get("month_id")
        month_goal = self.get_object(month_goal_id)
        if not month_goal:
            return JsonResponse({"error": "MonthGoal not found."}, status=404)

        # 月目標を達成状態にする
        month_goal.mark_as_completed()
        return JsonResponse({"result": "問題なくリクエストきている"}, status=200)