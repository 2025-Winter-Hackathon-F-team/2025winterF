import logging
from datetime import date

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from goal.models.month_goal import MonthGoal
from goal.models.todo import Todos
from goal.models.year_goal import YearGoal
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)


class MontGoalDetailView(LoginRequiredMixin, DetailView):
    template_name = "month_goal_detail.html"
    model = MonthGoal
    context_object_name = "month_goal"

    def get_object(self):
        """
        URLのパスから年を取得し、その年の年目標を取得する
        Returns:
            month_goal: 指定された年の月目標が存在すれば MonthGoal インスタンスを返す
        """
        year = self.kwargs.get("year", date.today().year)
        month = self.kwargs.get("month")

        # URL パラメータに month が設定されているか確認
        if not month:
            logger.warning(f"Month not provided in URL: year={year}")
            return None

        # 年をdatetime.dateに変換
        year_start_date = date(year, 1, 1)
        # 指定された年の目標を取得
        year_goal = YearGoal.get_year_goal_for_user(self.request.user, year_start_date)
        if not year_goal:
            logger.warning(
                f"[YearGoal] Not found: user_id={self.request.user.id}, year={year}"
            )
            return None

        # 月目標を取得
        month_goal = MonthGoal.get_specific_month_goal(year_goal=year_goal, month=month)

        return month_goal

    def get(self, request, *args, **kwargs):
        """
        GETリクエスト時に、目標が存在しない場合はリダイレクト
        """
        self.object = self.get_object()
        if self.object is None:
            messages.warning(
                request,
                f"{self.kwargs.get('year', date.today().year)}年の{self.kwargs.get('month')}月の目標はまだ設定されていません。",
            )
            return redirect(reverse("goal:home"))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストデータを作成する

        Returns:
            dict: テンプレートに渡すコンテキストデータ
        """
        context = super().get_context_data(**kwargs)
        month_goal = self.object

        if not month_goal:
            return context

        # month_goal に紐づくTodoを取得し、コンテキストに追加
        todos = Todos.get_todos_for_month_goal(month_goal)
        paginator = Paginator(todos, 6)  # １ページあたりの件数
        page_number = self.request.GET.get(
            "page"
        )  # URLのパラメータから現在のページ番号を取得
        page_obj = paginator.get_page(page_number)  # 指定ページのオブジェクトを返す
        context["todos"] = page_obj

        return context
