from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models.user_models import User
from ..models.year_goal import YearGoal
from ..models.month_goal import MonthGoal
from ..models.todo import Todos
from django.core.paginator import Paginator


# TODO: ホーム画面を表示するビューを作成（仮対応）
# DetailViewからTemplateViewに変更
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    # model = User

    def get_object(self):
        """
        現在ログインしているユーザーオブジェクトを取得する。
        Returns:
            User: ログイン中のユーザー。
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストデータを取得する。
        Returns:
            dict: コンテキストデータ。
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # 今年の目標（1件のみ取得）
        year_goal = YearGoal.get_current_year_goal(user)
        context["year_goal"] = year_goal

        # 今月の目標（1件のみ取得）
        month_goal = MonthGoal.get_current_month_goal(user)
        context["month_goal"] = month_goal

        # 今月のToDo（すべて取得 & ページネーション）
        todos = Todos.get_current_month_todos(user)
        paginator = Paginator(todos, 3)  # １ページあたり４件
        page_number = self.request.GET.get("page")  # URLのパラメータから現在のページ番号を取得
        page_obj = paginator.get_page(page_number)  # 指定ページのオブジェクトを返す
        context["todos"] = page_obj

        return context
