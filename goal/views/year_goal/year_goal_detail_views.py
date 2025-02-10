import logging
from datetime import date

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from goal.models import YearGoal
from goal.models.month_goal import MonthGoal


logger = logging.getLogger(__name__)

class YearGoalDetailView(LoginRequiredMixin, DetailView):
    template_name = "year_goal_detail.html"
    model = YearGoal
    context_object_name = "year_goal"

    def get_object(self):
        """
        URLのパスから年を取得し、その年の年目標を取得する
        Returns:
            YearGoal: 指定された年の年目標が存在すれば YearGoal インスタンスを返す
        """
        # URLパスから年を取得。指定されない場合は現在の年を使用
        year = self.kwargs.get("year", date.today().year)
        # 年をdatetime.dateに変換
        year_start_date = date(year, 1, 1)
        # 指定された年の目標を取得
        year_goal = YearGoal.get_year_goal_for_user(self.request.user, year_start_date)
        if not year_goal:
            logger.warning(f"[YearGoal] Not found: user_id={self.request.user.id}, year={year}")
            return None

        return year_goal

    def get(self, request, *args, **kwargs):
        """
        GETリクエスト時に、目標が存在しない場合はリダイレクト
        """
        self.object = self.get_object()
        if self.object is None:
            messages.warning(request, f"{self.kwargs.get('year', date.today().year)}年の目標はまだ設定されていません。")
            return redirect(reverse("goal:home"))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストデータを作成する

        Returns:
            dict: テンプレートに渡すコンテキストデータ
        """
        context = super().get_context_data(**kwargs)
        year_goal = self.object

        if not year_goal:
            return context

        # year_goal.id をキーとして月次目標を取得し、コンテキストに追加
        context["month_goals"] = MonthGoal.get_monthly_goals_for_year(year_goal_id=year_goal.id)

        return context