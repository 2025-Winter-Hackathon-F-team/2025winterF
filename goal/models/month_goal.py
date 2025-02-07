from django.db import models
from .year_goal import YearGoal

# month_goalsテーブルの作成
class MonthGoal(models.Model):
    # 目標の達成状況を表す定数
    STATUS_UNACHIEVED = 0
    STATUS_ACHIEVED = 1

    # statusフィールドの選択肢 (DB保存値, 表示文字列)
    STATUS_CHOICES = [
        (STATUS_UNACHIEVED, "未達"),
        (STATUS_ACHIEVED, "達成")
    ]

    # 月を表す定数
    MONTH_JANUARY = 1
    MONTH_FEBRUARY = 2
    MONTH_MARCH = 3
    MONTH_APRIL = 4
    MONTH_MAY = 5
    MONTH_JUNE = 6
    MONTH_JULY = 7
    MONTH_AUGUST = 8
    MONTH_SEPTEMBER = 9
    MONTH_OCTOBER = 10
    MONTH_NOVEMBER = 11
    MONTH_DECEMBER = 12

    # monthフィールドの選択肢 (DB保存値, 表示文字列)
    MONTH_CHOICES = [
        (MONTH_JANUARY, "1月"),
        (MONTH_FEBRUARY, "2月"),
        (MONTH_MARCH, "3月"),
        (MONTH_APRIL, "4月"),
        (MONTH_MAY, "5月"),
        (MONTH_JUNE, "6月"),
        (MONTH_JULY, "7月"),
        (MONTH_AUGUST, "8月"),
        (MONTH_SEPTEMBER, "9月"),
        (MONTH_OCTOBER, "10月"),
        (MONTH_NOVEMBER, "11月"),
        (MONTH_DECEMBER, "12月")
    ]

    # FK: year_goal_id INT NOT NULL
    year_goal = models.ForeignKey(YearGoal, null=False, on_delete=models.CASCADE, verbose_name="年目標")
    # month PositiveSmallIntegerField NOT NULL
    month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES, null=False, verbose_name="月")
    # title VARCHAR(50) Default NULL
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name="月の目標を入力してください")
    # status PositiveSmallIntegerField NOT NULL DEFAULT 0
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, null=False, default=STATUS_UNACHIEVED, verbose_name="達成状況")
    # created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    # updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        db_table="month_goals"
        unique_together = ('year_goal', 'month')
        verbose_name="月目標"
        verbose_name_plural = "月目標一覧"

    def __str__(self):
        year_goal_title = getattr(self.year_goal, 'title', 'Unknown Title')
        return f"{year_goal_title} - {self.title} ({self.month}月)"