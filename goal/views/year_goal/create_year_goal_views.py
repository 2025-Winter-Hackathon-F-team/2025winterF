from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from ...forms import YearGoalForm

from ...models import YearGoal

class CreateYearGoalView(FormView):
    model = YearGoal
    form_class = YearGoalForm
    template_name = 'year_goal_create.html'
    success_url = reverse_lazy('goal:home')

    def form_valid(self, form):
        user = self.request.user
        YearGoal.objects.create(
            user=user,
            title=form.cleaned_data['title']
        )
        return super().form_valid(form)