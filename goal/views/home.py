from django.shortcuts import render
from django.views.generic import TemplateView


# TODO: ホーム画面を表示するビューを作成（仮対応）
class HomeView(TemplateView):
    template_name = "home.html"