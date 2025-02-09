from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

from ..models import Message

logger = logging.getLogger(__name__)
logger.warning("危ない")


class FeedbackView(LoginRequiredMixin, TemplateView):
    template_name = "feedback.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message = Message.objects.first()

        # デバッグログを追加
        print("DEBUG: Retrieved Message:", message)

        context["message"] = message
        context["default_message"] = "メッセージが見つかりません。"
        return context
