from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from ..forms import LoginForm

class LoginView(LoginView):
    template_name = "login.html"
    form_class = LoginForm

    def get_success_url(self):
        """
        ログイン成功時にユーザーの状態に応じて遷移先を変更する
        Returns:
            str: 遷移先のURL（初回ログイン時は設定画面、それ以外はホーム）
        """
        user = self.request.user

        if user.is_first_login:
            # 初回ログイン時は設定画面へリダイレクト
            return reverse_lazy("account:setup")
        else:
            # 2回目以降のログインはホーム画面へリダイレクト
            return reverse_lazy("goal:home")