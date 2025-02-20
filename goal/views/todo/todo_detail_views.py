import logging
from datetime import date

from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from goal.models.month_goal import MonthGoal
from goal.models.todo import Todos
from goal.models.year_goal import YearGoal

logger = logging.getLogger(__name__)

class TodoDetailView(LoginRequiredMixin, DetailView):
    template_name = "todo_detail.html"
    model = Todos
    context_object_name = "todo"

    def get_object(self):
        """
        URLのパスから年、月、Todo(id)を取得し、Todoを取得する
        Returns:
            Todos: 指定されたTodoが存在すれば Todos インスタンスを返す
        """
        year = self.kwargs.get("year", date.today().year)
        month = self.kwargs.get("month")
        todo_id = self.kwargs.get("todo")

        # 年をdatetime.dateに変換
        year_start_date = date(year, 1, 1)
        # 指定された年の目標を取得
        year_goal = YearGoal.get_year_goal_for_user(self.request.user, year_start_date)
        if not year_goal:
            logger.warning(f"[YearGoal] Not found: user_id={self.request.user.id}, year={year}")
            return None

        # URL パラメータに month が設定されているか確認
        if not month:
            logger.warning(f"Month not provided in URL: year={year}")
            return None

        # 月目標を取得
        month_goal = MonthGoal.get_specific_month_goal(year_goal=year_goal, month=month)
        if not month_goal:
            logger.warning(f"[MonthGoal] Not found: user_id={self.request.user.id}, year_goal.id={year_goal.id}, month={month}")
            return None

        # Todo を取得
        todo = Todos.get_specific_todo(month_goal=month_goal, todo_id=todo_id)

        return todo

    def get(self, request, *args, **kwargs):
        """
        GETリクエスト時に、目標が存在しない場合はリダイレクト
        """
        self.object = self.get_object()
        if self.object is None:
            year = self.kwargs.get("year", date.today().year)
            month = self.kwargs.get("month")
            todo_id = self.kwargs.get("todo")
            messages.warning(request, f"{year}年の{month}月の指定したTodo（id={todo_id}）はまだ設定されていません。")
            return redirect(reverse("goal:month_goal_detail_specific_year", kwargs={"year": year, "month": month}))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストデータを作成する

        Returns:
            dict: テンプレートに渡すコンテキストデータ
        """
        context = super().get_context_data(**kwargs)
        return context


