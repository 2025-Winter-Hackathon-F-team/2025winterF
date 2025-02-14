from django.db import models

from .month_goal import MonthGoal

# todosテーブルの作成
class Todos(models.Model):
    # 目標の達成状況を表す定数
    STATUS_UNACHIEVED = 0
    STATUS_ACHIEVED = 1

    # statusフィールドの選択肢 (DB保存値, 表示文字列)
    STATUS_CHOICES = [
        (STATUS_UNACHIEVED, "未達"),
        (STATUS_ACHIEVED, "達成")
    ]

    # FK: month_goal_id INT NOT NULL
    month_goal = models.ForeignKey(MonthGoal, null=False, on_delete=models.CASCADE)
    # title VARCHAR(50) NOT NULL
    title = models.CharField(max_length=50, null=False, verbose_name="日々のタスクを入力してください")
    # status PositiveSmallIntegerField NOT NULL DEFAULT 0
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, null=False, default=STATUS_UNACHIEVED,  verbose_name="達成状況")
    # created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    # updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        db_table="todos"
        verbose_name="TODO"
        verbose_name_plural = "TODO一覧"

    def __str__(self):
        month_goal_title = getattr(self.month_goal, 'title', 'Unknown Title')
        return f"{month_goal_title} - {self.title}"

    @classmethod
    def get_current_month_todos(cls, user):
        """
        現在の月のToDoを全件取得
        Args:
            user: ログインユーザー
        Returns:
            QuerySet: 今月のToDoリスト
        """
        month_goal = MonthGoal.get_current_month_goal(user)

        if month_goal is None:
            return cls.objects.none()
        return cls.objects.filter(month_goal=month_goal).order_by("created_at")
