from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .forms import SignUpForm, LoginForm
from .models import User

class SignUpView(FormView):
    template_name = "signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        """
        フォームが有効な場合に呼び出され、ユーザーを作成する。
        Args:
            form (SignUpForm): 送信されたフォーム。
        Returns:
            HttpResponseRedirect: リダイレクトレスポンス (成功時)。
            HttpResponse: フォームを含むレスポンス (失敗時)。
        Raises:
            IntegrityError: メールアドレスの重複登録が発生した場合。
            ValueError: その他のバリデーションエラーが発生した場合。
        """
        try:
            User.objects.create_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
        except IntegrityError:
            form.add_error("email", "このメールアドレスはすでに登録されています")
        except ValidationError as e:
            for message in e.messages:
                form.add_error("password", message)
            if form.errors:
                return self.form_invalid(form)

        return super().form_valid(form)

class LoginView(LoginView):
    template_name = "login.html"
    form_class = LoginForm