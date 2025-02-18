from datetime import date
import logging

from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from goal.forms.todo.todo_forms import TodoForm
from ...models import YearGoal, MonthGoal, Todos

logger = logging.getLogger(__name__)

class TodoCreateView(LoginRequiredMixin, FormView):
    model = Todos
    template_name = "todo_create.html"
    form_class = TodoForm

    def form_valid(self, form):
        """
        フォームが正常に送信された場合に呼び出され、Todoの作成を行うメソッド。
        - ログインユーザーを取得し、指定された年と月に対応する年目標および月目標を取得。
        - フォームから取得したタイトルを使って、Todoを作成します。

        Returns:
            HttpResponseRedirect: form_validが正常に実行されると、フォームの送信後に成功ページへリダイレクトされます。
        """
        user = self.request.user
        # 年が指定されていなければ現在の年を使用
        year = self.kwargs.get('year', date.today().year)
        month = self.kwargs.get("month")

        year_start_date = date(year, 1, 1)

        # 年目標を取得
        year_goal = YearGoal.get_year_goal_for_user(user=user, year=year_start_date)
        if not year_goal:
            logger.warning(f"[YearGoal] Not found: user_id={self.request.user.id}, year={year}")
            form.add_error(None, f"指定された年目標（{year}）が見つかりませんでした。")
            return self.form_invalid(form)
        # 月目標を取得
        month_goal = MonthGoal.get_specific_month_goal(year_goal=year_goal, month=month)
        if not month_goal:
            logger.warning(f"[MonthGoal] Not found: user_id={self.request.user.id}, year_goal={year_goal}, month={month}")
            form.add_error(None, f"指定された月目標（{month}月）が見つかりませんでした。もう一度お試しください。")
            return self.form_invalid(form)

        title = form.cleaned_data["title"]
        try:
            # Todoを作成
            Todos.create_todo(title=title, month_goal=month_goal)
        except Exception as e:
            logger.exception(f"Todoの作成中にエラーが発生しました: {e}")
            form.add_error(None, "Todoの作成に失敗しました。もう一度お試しください。")
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        # エラーメッセージをビューで表示
        return super().form_invalid(form)

    def get_success_url(self):
        """
        Todo作成後、遷移先のURLを決定するメソッド。
        - 年が指定されている場合は、指定された年と月に対応する月目標詳細画面へ遷移。
        - 年が指定されていない場合は、現在の年の月目標詳細画面へ遷移。

        Returns:
            str: 遷移先のURL。年が指定されていれば、指定された年と月に対応する月目標詳細画面へ、
                そうでなければ現在の年の月目標の詳細画面へ遷移します。
        """
        year = self.kwargs.get('year')
        month = self.kwargs.get("month")

        if year:
            return reverse("goal:month_goal_detail_specific_year", kwargs={"year": year, "month": month})
        else:
            return reverse("goal:month_goal_detail", kwargs={"month": month})