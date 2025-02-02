from django.db import models
from django.utils import timezone
import datetime
from account.models import User

# 現在の年の初日をデフォルト値として返す関数
def default_year_start():
    current_year = timezone.now().year
    return datetime.date(current_year, 1, 1)

# year_goalsテーブルの作成
class YearGoal(models.Model):
    # 目標の達成状況を表す定数
    STATUS_UNACHIEVED = 0
    STATUS_ACHIEVED = 1

    # statusフィールドの選択肢 (DB保存値, 表示文字列)
    STATUS_CHOICES = [
        (STATUS_UNACHIEVED, "未達"),
        (STATUS_ACHIEVED, "達成")
    ]

    # FK: user_id INT NOT NULL
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー")
    # year DATE NOT NULL 年の初日をデフォルト値として設定
    year = models.DateField(default=default_year_start, verbose_name="年目標")
    # title VARCHAR(50) NOT NULL
    title = models.CharField(max_length=50, verbose_name="年間目標を入力してください")
    # status PositiveSmallIntegerField NOT NULL DEFAULT 0
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_UNACHIEVED, verbose_name="達成状況")
    # created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    # updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        db_table="year_goals"
        verbose_name="年目標"
        verbose_name_plural="年目標一覧"

    def __str__(self):
        user_email = getattr(self.user, 'email', 'Unknown Email')
        return f"{self.year.year} - {self.title} ({user_email})"

    # 目標の作成メソッド
    def create(self, user, year, title):
        self.user = user
        self.year = year
        self.title = title
        self.save()