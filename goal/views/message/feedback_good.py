from random import choice

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ...models import Message


class FeedbackGoodView(LoginRequiredMixin, TemplateView):
    template_name = "feedback_good.html"
    model = Message

    DEFAULT_PRAISE_MESSAGE = "今日は勝利、だが死神は次も待っているぞ。"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        praise_messages = Message.get_praise_messages()

        context["praise_message"] = (
            self.get_random_praise_message(praise_messages)
            if praise_messages.exists()
            else self.DEFAULT_PRAISE_MESSAGE
        )

        return context

    def get_random_praise_message(self, messages):
        """
        お褒めの言葉をランダムに取得する

        Args:
            messages(QuerySet(Message)): お褒めの言葉一覧

        Returns:
            message(Message): ランダムに取得したお褒めの言葉
        """
        return choice(messages)
