from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError
from django.core.exceptions import ValidationError

from ..forms import SetupForm
from ..models import User

class SetupView(LoginRequiredMixin, UpdateView):
    template_name = "setup.html"
    form_class = SetupForm
    model = User
    success_url = reverse_lazy('goal:home')

    def get_object(self):
        """
        現在ログインしているユーザーオブジェクトを取得する。
        Returns:
            User: ログイン中のユーザー。
        """
        return self.request.user

    def form_valid(self, form):
        """
        フォーム送信後に有効な場合に呼び出される。
        ユーザー情報を更新する処理を実行。
        Args:
            form (InitialSetupForm): フォームから送信されたデータ。
        Returns:
            HttpResponseRedirect: 成功時のリダイレクトレスポンス。
            HttpResponse: フォームを含むレスポンス (失敗時)。
        """
        try:
            # プロフィール情報を更新
            self.get_object().update_profile_initial(
                name=form.cleaned_data["name"],
                birthday=form.cleaned_data["birthday"],
                deathday=form.cleaned_data["deathday"],
            )
            return super().form_valid(form)
        except ValidationError as e:
            # バリデーションエラーの場合、フォームにエラーを追加
            form.add_error(None, "入力内容に誤りがあります。ご確認の上、再度お試しください。")
        except DatabaseError as e:
            # データベースエラーの場合、フォームにエラーを追加
            form.add_error(None, "現在、データベースの処理中に問題が発生しています。時間をおいて再試行してください。")
        except Exception as e:
            # その他の予期しないエラーもフォームに追加
            form.add_error(None, "システムエラーが発生しました。時間をおいて再試行してください。")

        # エラーが発生した場合、フォームを含むレスポンスを返す
        return self.form_invalid(form)