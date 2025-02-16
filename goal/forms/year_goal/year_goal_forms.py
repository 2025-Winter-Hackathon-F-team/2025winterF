from ...models import YearGoal
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class YearGoalForm(forms.ModelForm):
    class Meta:
        model = YearGoal
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # requestを受け取る
        super().__init__(*args, **kwargs)

    def clean_title(self):
        # タイトルの値を確認
        title = self.cleaned_data.get("title")
        """
        Return: titleを返す
        Raises: 
            タイトル空白: forms.ValidationError: 文字を入れてください
            タイトルスペースのみ: form.ValidationError: 入力できない文字列です
            タイトル50字以上: forms.ValidationError: ５０字以内で入力してください
        """
        if not isinstance(title, str):
            raise forms.ValidationError("タイトルは文字列で入力してください。")
        if not (title := title.strip()):
            raise forms.ValidationError(
                "タイトルは空白文字のみで入力しないでください。"
            )
        if len(title) > 50:
            raise forms.ValidationError("タイトルは50文字以内で入力してください。")
        return title

    def clean(self):
        cleaned_data = super().clean()
        if self.request and self.request.user.is_authenticated:
            user = self.request.user
            # 現在の年の最初の日付と最後の日付を取得
            current_year = timezone.now().year
            current_year_str = f"{current_year}-01-01"  # 文字列に変換
            if YearGoal.objects.filter(user=user, year=current_year_str).exists():
                raise ValidationError(f"{current_year}年の目標は既に登録されています。")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            instance.user = self.request.user
        if commit:
            instance.save()
        return instance
