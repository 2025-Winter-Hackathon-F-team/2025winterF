from ...models import YearGoal
from django import forms
import datetime


class YearGoalForm(forms.ModelForm):
    class Meta:
        model = YearGoal
        fields = ["title"]

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

    # def clean(self):
    #     return super().clean()
