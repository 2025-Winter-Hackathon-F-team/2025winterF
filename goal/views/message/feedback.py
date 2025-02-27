from random import choice

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ...models import Message


class FeedbackView(LoginRequiredMixin, TemplateView):
    template_name = "feedback.html"
    model = Message

    DEFAULT_SCOLD_MESSAGE = "勝利は遠い、だが命の灯火はまだ消えていない。"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scold_messages = Message.get_scold_messages()

        context["scold_message"] = (
            self.get_random_scold_message(scold_messages)
            if scold_messages.exists()
            else self.DEFAULT_SCOLD_MESSAGE
        )

        return context

    def get_random_scold_message(self, messages):
        """
        お叱りの言葉をランダムに取得する

        Args:
            messages(QuerySet(Message)): お叱りの言葉一覧

        Returns:
            message(Message): ランダムに取得したお褒めの言葉
        """
        return choice(messages)

