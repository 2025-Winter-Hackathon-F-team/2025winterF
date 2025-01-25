from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import User

class SignUpForm(forms.ModelForm):
    """
    ユーザー登録フォーム。
    メールアドレス、パスワード、パスワード確認の入力を受け付ける。
    """
    email = forms.EmailField(
        label="メールアドレス",
        error_messages={"required": "メールアドレスの入力は必須です。"},
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        error_messages={"required": "パスワードの入力は必須です。"},
    )
    password_confirm = forms.CharField(
        label="パスワード確認",
        widget=forms.PasswordInput,
        error_messages={"required": "確認パスワードの入力は必須です。"},
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        """
        メールアドレスの一意性を検証するメソッド。
        Returns:
            email: 検証済みのメールアドレス。
        Raises:
            forms.ValidationError: 同じメールアドレスが既に登録されている場合。
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています。")
        return email

    def clean(self):
        """
        パスワードの確認とバリデーションを行うメソッド。
        Returns:
            cleaned_data: 検証済みのデータを含む辞書。
        Raises:
            forms.ValidationError: 以下のいずれかの場合に発生。
                - パスワードと確認用パスワードが一致しない場合。
                - パスワードが Django のパスワードバリデーションに失敗した場合（例：短すぎる、一般的すぎるなど）。
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # パスワードと確認用パスワードが一致しない場合
        if password != password_confirm:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません。")

        # パスワードのバリデーション
        if password:
            try:
                validate_password(password)
            except forms.ValidationError as e:
                for message in e.messages:
                    self.add_error("password", message)

        return cleaned_data