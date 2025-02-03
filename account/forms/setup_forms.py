from datetime import date
from django import forms

from ..models import User

class SetupForm(forms.ModelForm):
    """
    初期設定フォーム。
    名前、誕生日、寿命（何歳まで生きたいか）を入力。
    """
    name = forms.CharField(
        label="あなたの名前",
        required=True
    )
    birth_date = forms.DateField(
        label="誕生日",
        widget=forms.DateInput(attrs={"type": "date"}),
        required=True
    )
    # IntegerField で寿命を受け取る
    lifespan_end_date = forms.IntegerField(
        label="何歳まで生きたい？",
        required=False,
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={"step": "1"})
    )

    class Meta:
        model = User
        fields = ("name", "birth_date", "lifespan_end_date")

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
        birth_date = cleaned_data.get("birth_date")
        lifetime = cleaned_data.get("lifespan_end_date")

        # 名前のバリデーション
        if not name:
            self.add_error("name", "お名前を入力してください。")

        # 誕生日のバリデーション
        if not birth_date:
            self.add_error("birth_date", "誕生日を入力してください。")
        elif birth_date > date.today():
            self.add_error("birth_date", "誕生日は未来の日付に設定できません。")

        # 寿命の入力が小数の場合
        if lifetime is not None and lifetime % 1 != 0:
            self.add_error("lifespan_end_date", "寿命は整数で入力してください。")

        # 寿命のバリデーション
        if lifetime:
            if lifetime <= 0:
                self.add_error("lifespan_end_date", "寿命は正の整数で入力してください。")
            elif lifetime > 120:
                self.add_error("lifespan_end_date", "寿命は120歳以下で入力してください。")
            if lifetime <= 0:
                self.add_error("lifespan_end_date", "寿命は正の整数で入力してください。")
            else:
                try:
                    # ユーザーが入力した年齢を誕生日に加算して死亡日を計算
                    calculated_lifespan_end_date = date(
                        birth_date.year + lifetime,
                        birth_date.month,
                        birth_date.day
                    )
                    if calculated_lifespan_end_date <= date.today():
                        self.add_error("lifespan_end_date", "寿命の年齢は現在より未来の年齢に設定してください。")
                    else:
                        # cleaned_data を直接変更せず、新しい辞書を返す
                        return {**cleaned_data, "lifespan_end_date": calculated_lifespan_end_date}
                except ValueError as e:
                    # 無効な日付計算の場合（例: うるう年など）
                    print(f"Error calculating lifespan_end_date: {e}")
                    self.add_error("lifespan_end_date", "寿命の計算に失敗しました。誕生日と寿命の入力を再確認してください。")
        else:
            # 寿命が未入力の場合、デフォルト値を設定
            cleaned_data["lifespan_end_date"] = None
        return cleaned_data