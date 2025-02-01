from datetime import date
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from dateutil.relativedelta import relativedelta

from ..models import User

class ProfileView(LoginRequiredMixin, DetailView):
    template_name = "profile.html"
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
        # get_objectで取得したユーザーオブジェクト
        user = self.object
        # ユーザーの年齢と寿命を計算
        context["age"] = (
            relativedelta(date.today(), user.birthday).years
            if user.birthday
            else None
        )
        context["life_span"] = (
            relativedelta(user.deathday, user.birthday).years
            if user.birthday and user.deathday
            else None
        )

        return context