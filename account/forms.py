from datetime import date
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

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


class InitialSetupForm(forms.ModelForm):
    """
    初期設定フォーム。
    名前、誕生日、寿命（何歳まで生きたいか）を入力。
    """
    name = forms.CharField(
        label="あなたの名前",
        required=True
    )
    birthday = forms.DateField(
        label="誕生日",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    # IntegerField で寿命を受け取る
    deathday = forms.IntegerField(
        label="何歳まで生きたい？",
        required=False,
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={'step': '1'})
    )

    class Meta:
        model = User
        fields = ("name", "birthday", "deathday")

    def clean(self):
        """
        フォーム全体のバリデーション。
        Returns:
            cleaned_data: 検証済みのデータを含む辞書。
        Raises:
            forms.ValidationError: データの整合性エラーが発生した場合。
        """
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        birthday = cleaned_data.get("birthday")
        lifetime = cleaned_data.get("deathday")

        # 名前のバリデーション
        if not name:
            self.add_error("name", "お名前を入力してください。")

        # 誕生日のバリデーション
        if not birthday:
            self.add_error("birthday", "誕生日を入力してください。")
        elif birthday > date.today():
            self.add_error("birthday", "誕生日は未来の日付に設定できません。")

        # 寿命の入力が小数の場合
        if lifetime is not None and lifetime % 1 != 0:
            self.add_error("deathday", "寿命は整数で入力してください。")

        # 寿命のバリデーション
        if lifetime:
            if lifetime <= 0:
                self.add_error("deathday", "寿命は正の整数で入力してください。")
            elif lifetime > 120:
                self.add_error("deathday", "寿命は120歳以下で入力してください。")
            if lifetime <= 0:
                self.add_error("deathday", "寿命は正の整数で入力してください。")
            else:
                try:
                    # ユーザーが入力した年齢を誕生日に加算して死亡日を計算
                    calculated_deathday = date(
                        birthday.year + lifetime,
                        birthday.month,
                        birthday.day
                    )
                    if calculated_deathday <= date.today():
                        self.add_error("deathday", "寿命の年齢は現在より未来の年齢に設定してください。")
                    else:
                        # cleaned_data を直接変更せず、新しい辞書を返す
                        return {**cleaned_data, "deathday": calculated_deathday}
                except ValueError as e:
                    # 無効な日付計算の場合（例: うるう年など）
                    print(f"Error calculating deathday: {e}")
                    self.add_error("deathday", "寿命の計算に失敗しました。誕生日と寿命の入力を再確認してください。")
        else:
            # 寿命が未入力の場合、デフォルト値を設定
            cleaned_data["deathday"] = None
        return cleaned_data