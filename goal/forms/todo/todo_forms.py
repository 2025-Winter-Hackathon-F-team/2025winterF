from django import forms

from ...models import Todos

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todos
        fields = ("title",)

    def clean_title(self):
        """
        タイトルのバリデーションを行う。
        Returns:
            str: title

        Raises:
            forms.ValidationError: タイトルが空白文字のみの場合にエラーを発生させる。
        """
        title = self.cleaned_data.get("title", "")
        checkTitle = title.strip()

        if not checkTitle:
            raise forms.ValidationError("タイトルは空白文字のみで入力しないでください。")

        return title

