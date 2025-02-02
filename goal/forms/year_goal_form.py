from ..models import YearGoal
from django import forms

class YearGoalForm(forms.ModelForm):
    class Meta:
        model = YearGoal
        fields = ['title']

    def clean(self):
        return super().clean()