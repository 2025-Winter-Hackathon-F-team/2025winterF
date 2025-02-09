from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from ...forms import YearGoalForm
from ...models import YearGoal, MonthGoal

import logging #TODO: コミット前に削除

logger = logging.getLogger(__name__)

"""
    年間目標を追加するビュー
"""


class CreateYearGoalView(LoginRequiredMixin, FormView):
    model = YearGoal
    form_class = YearGoalForm
    template_name = "year_goal_create.html"
    success_url = reverse_lazy("goal:home")

    def form_valid(self, form):
        user = self.request.user
        # 年目標を作成
        year_goal = YearGoal.objects.create(user=user, title=form.cleaned_data["title"])
        # 月目標を作成
        MonthGoal.create_monthly_goals_for_year(year_goal.id)
        return super().form_valid(form)
