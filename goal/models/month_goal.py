import datetime
import logging

from django.db import models, DatabaseError
from django.utils import timezone

from .year_goal import YearGoal

logger = logging.getLogger(__name__)

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

    @classmethod
    def create_month_goal(cls, month, year_goal_id):
        """
        指定された月の目標を作成するメソッド。
        Args:
            month (int): 月
            year_goal_id (int): 年目標の主キー
        Returns:
            None
        Raises:
            DatabaseError: データベースエラーが発生した場合
            Exception: その他の予期しないエラー
        """
        try:
            _, created = cls.objects.get_or_create(month=month, year_goal_id=year_goal_id)
            if created:
                logger.debug(f"Created goal for {month} in YearGoal ID: {year_goal_id}")
            else:
                logger.debug(f"Goal for {month} already exists in YearGoal ID: {year_goal_id}")
        except DatabaseError as e:
            # データベースエラーの内容を出力
            logger.error(f"Database error occurred while creating goal for {month} in YearGoal ID: {year_goal_id}. Error: {str(e)}")
            raise
        except Exception as e:
            # その他のエラー内容を出力
            logger.exception(f"Unexpected error occurred while creating goal for {month} in YearGoal ID: {year_goal_id}.")
            raise

    @classmethod
    def create_monthly_goals_for_year(cls, year_goal_id):
        """
        指定された YearGoal に対して、当月から12月までの月目標を作成する
        Args:
            year_goal_id (int): 年目標の主キー
        Returns:
            None
        """
        current_month = datetime.datetime.now().month
        for month in range(current_month, 13):
            try:
                cls.create_month_goal(month, year_goal_id)
            except DatabaseError:
                logger.error(f"Skipping month {month} due to database error.")
            except Exception:
                logger.exception(f"Skipping month {month} due to unexpected error.")

    @classmethod
    def get_monthly_goals_for_year(cls, year_goal_id):
        """
        指定された YearGoal に対して、すべての月目標を取得しリストとして返す
        Args:
            year_goal_id (int): 年目標の主キー
        Returns:
            list: 月目標のリスト（辞書形式）
        """
        try:
            monthly_goals = cls.objects.filter(year_goal=year_goal_id).order_by('month')
        except DatabaseError:
            logger.error(f"Database error while fetching monthly goals for YearGoal ID {year_goal_id}.")
            return []
        except Exception as e:
            logger.exception(f"Unexpected error while fetching monthly goals for YearGoal ID {year_goal_id}: {e}")
            return []

        # 月の選択肢（表示用の辞書）を取得
        month_choices_dict = dict(cls.MONTH_CHOICES)

        # 各月目標を辞書形式でリストに追加
        return [
            {
                "month": month_choices_dict.get(goal.month, "N/A"),  # 月
                "title": goal.title,  # タイトル
                "status": goal.status,  # 状態
            }
            for goal in monthly_goals
        ]

    @classmethod
    def get_current_month_goal(cls, user):
        """
        YearGoal.year=現在の年となる年目標1件を取得する
        MonthGoal.month=現在の月となる月目標1件を取得する
            Args:
                user: ログインユーザー
            Returns:
                MonthGoal.year=現在の月となる月目標1件
        """
        current_month = timezone.now().month

        year_goal = YearGoal.get_current_year_goal(user)

        if year_goal is None :
            return None
        return cls.objects.filter(
            year_goal=year_goal, month=current_month
        ).first()

    @classmethod
    def get_specific_month_goal(cls, year_goal, month):
        """
        指定された特定の年、月の目標を取得する
        Args:
            year_goal (YearGoal): 年目標
            month (int): 目標を取得する月
        Returns:
            MonthGoal or None: 該当する月目標が存在すれば MonthGoal インスタンスを返し、存在しなければ None を返す
        """
        try:
            return cls.objects.get(year_goal = year_goal, month=month)
        except cls.DoesNotExist as e:
            # 目標が設定されていない場合、ログに記録して None を返す
            logger.warning(f"[MonthGoal] Not found: year_goal_id={year_goal.id}, month={month}. Error: {e}")
            return None
        except cls.MultipleObjectsReturned as e:
            # データの整合性エラー（1つの年の1つの月に複数の目標が存在する）
            logger.error(f"[MonthGoal] Data integrity issue: Multiple entries found for year_goal_id={year_goal.id}, month={month}. Error: {e}")
            return None
        except DatabaseError as e:
            # データベース関連のエラー
            logger.error(f"[MonthGoal] DatabaseError: year_goal_id={year_goal.id}, month={month}. Error: {e}")
            return None
        except Exception as e:
            # 予期しないエラーのキャッチ
            logger.exception(f"[MonthGoal] Unexpected error: year_goal_id={year_goal.id}, month={month}. Error: {e}")
            return None