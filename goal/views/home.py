from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models.user_models import User


# TODO: ホーム画面を表示するビューを作成（仮対応）
class HomeView(LoginRequiredMixin, DetailView):
    template_name = "home.html"
    model = User

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
        return context
