import datetime
import logging
import json

from django.views.generic import UpdateView
from django.http import JsonResponse
from goal.forms.year_goal.year_goal_forms import YearGoalForm
from goal.models import YearGoal

logger = logging.getLogger(__name__)

class YearGoalUpdateView(UpdateView):
    model = YearGoal
    form_class = YearGoalForm

    def get_object(self, year):
        """
        更新対象の年目標を取得する
        Returns:
            YearGoal: 指定された年の年目標が存在すれば YearGoal インスタンスを返す
        """
        # 年をdatetime.dateに変換
        try:
            year = int(year)
            year_date = datetime.date(year, 1, 1)
        except ValueError:
            logger.warning(f"Invalid year parameter: {year}")
            return None

        # 指定された年の目標を取得
        year_goal = YearGoal.get_year_goal_for_user(self.request.user, year_date)
        if not year_goal:
            logger.warning(f"[YearGoal] Not found: user_id={self.request.user.id}, year={year}")
            return None

        return year_goal

    def post(self, request, *args, **kwargs):
        """
        年目標を更新するためのAPIエンドポイント
        Args:
            request (HttpRequest): クライアントからのリクエスト
        Returns:
            JsonResponse:
                - 成功時: 更新されたタイトルを返す (status=200)
                - 失敗時: エラーメッセージを返す (status=400)
        """
        try:
            # リクエストボディをJSONとして読み込む
            data = json.loads(request.body)
            logger.info(f"Received data: {data}")

            # "title" の取得
            newTitle = data.get("title")

            # "year" の取得とバリデーション
            year = data.get("year")
            if not year:
                logger.warning("Year parameter is missing.")
                return JsonResponse({"error": "Year parameter is required."}, status=400)

            # "YearGoal" の取得
            goal = self.get_object(year)
            if not goal:
                return JsonResponse({"error": "YearGoal not found."}, status=404)

            logger.info(f"Updating YearGoal for year {year} and user {request.user}")

            # "YearGoalForm" でバリデーション
            form = self.form_class(data={"title": newTitle}, instance=goal)

            if form.is_valid():
                try:
                    # 年目標を更新
                    goal.update_title(newTitle)
                    logger.info("Form validation successful. Data updated.")
                    return JsonResponse({"title": goal.title}, status=200)
                except Exception as e:
                    logger.error(f"Failed to update YearGoal: {e}")
                    return JsonResponse({"error": {"title": ["保存に失敗しました"]}}, status=400)
            else:
                logger.info(f"Form validation failed: {form.errors}")
                return JsonResponse({"error": form.errors}, status=400)

        except json.JSONDecodeError:
            logger.warning("Invalid JSON format in request body.")
            return JsonResponse({"error": {"title": ["保存に失敗しました"]}}, status=400)

        except Exception as e:
            logger.error(f"Unexpected error in YearGoalUpdateView: {e}")
            return JsonResponse({"error": {"title": ["保存に失敗しました"]}}, status=400)
