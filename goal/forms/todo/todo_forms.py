from django import forms

from ...models import Todos

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todos
        fields = ("title",)

    def clean_title(self):
        """
        タイトルのバリデーションを行う。
        Returns: titleを返す
        Raises:
            タイトル空白: forms.ValidationError: 文字を入れてください
            タイトルスペースのみ: form.ValidationError: 入力できない文字列です
            タイトル50字以上: forms.ValidationError: ５０字以内で入力してください
        """
        title = self.cleaned_data.get("title")

        if not isinstance(title, str):
            raise forms.ValidationError("タイトルは文字列で入力してください。")
        if not (title := title.strip()):
            raise forms.ValidationError(
                "タイトルは空白文字のみで入力しないでください。"
            )
        if len(title) > 50:
            raise forms.ValidationError("タイトルは50文字以内で入力してください。")

        return title

