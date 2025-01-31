from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    """
    ログインフォーム。
    メールアドレス、パスワードの入力を受け付ける。
    """
    def __init__(self, *args, **kwargs):
        """
        LoginForm の初期化。

        フィールドの初期設定を行います。

        設定内容:
            - username (EmailField): メールアドレス入力フィールド。autofocus 属性と必須エラーメッセージを設定。
            - password (CharField): パスワード入力フィールド。必須エラーメッセージを設定。
        """
        super().__init__(*args, **kwargs)
        self.fields['username'] = forms.EmailField(
            label='メールアドレス',
            widget=forms.EmailInput(attrs={"autofocus": True}),
            error_messages={"required": "メールアドレスを入力してください。"}
        )
        self.fields['password'].label = 'パスワード'
        self.fields['password'].error_messages = {"required": "パスワードを入力してください。"}