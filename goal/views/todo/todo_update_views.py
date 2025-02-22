import datetime
import json
import logging
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from goal.models.todo import Todos
from goal.models.month_goal import MonthGoal
from goal.models.year_goal import YearGoal

logger = logging.getLogger(__name__)


class TodoUpdateView(LoginRequiredMixin, View):
    """
    特定のTodoの更新を処理するビュー
    """

    def post(self, request, month, todo, year=None):
        print(
            f"✅ [DEBUG] TodoUpdateView にリクエストが到達: year={year}, month={month}, todo={todo}"
        )

        try:
            # リクエストボディをJSONとして読み込む
            data = json.loads(request.body)
            new_title = data.get("title")

            # 年目標を取得（year が None でなければ）
            year_goal = None
            if year is not None:
                try:
                    year = int(year)
                    year_date = datetime.date(year, 1, 1)
                    year_goal = YearGoal.get_year_goal_for_user(request.user, year_date)
                    if not year_goal:
                        return JsonResponse(
                            {"error": "Year goal not found"}, status=404
                        )
                except ValueError:
                    return JsonResponse({"error": "Invalid year format"}, status=400)

            # 月目標を取得
            month_goal = MonthGoal.get_specific_month_goal(year_goal, month)
            if not month_goal:
                return JsonResponse({"error": "Month goal not found"}, status=404)

            # Todo を取得
            todo_item = Todos.get_specific_todo(month_goal, todo)
            if not todo_item:
                return JsonResponse({"error": "Todo not found"}, status=404)

            # タイトルを更新
            todo_item.title = new_title
            todo_item.save()

            logger.info(f"Todo updated successfully: {todo_item}")
            return JsonResponse(
                {"message": "更新に成功しました", "title": new_title}, status=200
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({"error": "保存に失敗しました"}, status=500)
