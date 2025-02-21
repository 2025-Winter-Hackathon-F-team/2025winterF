import logging

from django.db import models, DatabaseError

from .month_goal import MonthGoal

logger = logging.getLogger(__name__)

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

    @classmethod
    def create_todo(cls, title, month_goal):
        """
        指定された月のToDoを作成
        Args:
            title: Todoのタイトル
            month_goal: 月目標
        """
        try:
            # 新しいTodoを作成
            cls.objects.create(title=title, month_goal=month_goal)
        except DatabaseError as e:
            logger.error(f"Database error occurred while creating Todo for MonthGoal ID {month_goal.id} with title '{title}': {e}")
            raise
        except Exception as e:
            logger.exception(f"An unexpected error occurred while creating Todo for MonthGoal ID {month_goal.id} with title '{title}': {e}")
            raise

    @classmethod
    def get_todos_for_month_goal(cls, month_goal):
        """
        指定された MonthGoal に対して、すべてのTodoを取得しリストとして返す
        Args:
            month_goal: 月目標
        Returns:
            QuerySet: Todo のクエリセット
        """
        try:
            todos = cls.objects.filter(month_goal=month_goal).order_by("id")
            return todos
        except DatabaseError:
            logger.error(f"Database error while fetching todos for MonthGoal ID {month_goal.id}.")
        except Exception as e:
            logger.exception(f"Unexpected error while fetching todos for MonthGoal ID {month_goal.id}: {e}")

        return cls.objects.none()

    @classmethod
    def has_unachieved(cls, month_goal):
        """
        指定された月目標に紐づく未達成のToDoが存在するかを確認する
        Args:
            month_goal (MonthGoal): チェックする対象の月目標
        Returns:
            bool: 未達成のToDoが存在すればTrue、それ以外はFalse
            None: エラーが発生した場合
        Raise:
            予期しないエラーのキャッチ場合
        """
        try:
            return cls.objects.filter(status=cls.STATUS_UNACHIEVED, month_goal=month_goal).exists()
        except cls.DoesNotExist:
            # 特定のオブジェクトが存在しない場合の処理
            logger.warning(f"[Todos] No month goal found: month_goal={month_goal.id}")
            return None
        except Exception as e:
            # 予期しないエラーのキャッチ
            logger.exception(f"[Todos] Unexpected error while checking unachieved todos for month_goal={month_goal.id}: {e}")
            raise

    @classmethod
    def mark_as_achieved_for_goal(cls, month_goal):
        """
        指定された月目標に紐づく未達成のToDoを達成済みに変更する
        Args:
            month_goal (MonthGoal): 対象の月目標
        Returns:
            int: 更新されたToDoの数
            None: エラーが発生した場合
        """
        try:
            updated_count = cls.objects.filter(status=cls.STATUS_UNACHIEVED, month_goal=month_goal).update(status=cls.STATUS_ACHIEVED)
            return updated_count
        except Exception as e:
            logger.exception(f"[Todos] Unexpected error while marking todos as achieved for month_goal={month_goal.id}: {e}")
            return None

    @classmethod
    def get_specific_todo(cls, month_goal, todo_id):
        """
        指定されたTodoを取得する
        Args:
            month_goal (MonthGoal): 月目標
            todo_id (int): Todoのid
        Returns:
            Todo or None: 該当するTodoが存在すれば Todos インスタンスを返し、存在しなければ None を返す
        """
        try:
            return cls.objects.get(month_goal=month_goal, id=todo_id)
        except cls.DoesNotExist as e:
            # 目標が設定されていない場合、ログに記録して None を返す
            logger.warning(f"[Todo] Not found: month_goal_id={month_goal.id}, todo_id={todo_id}. Error: {e}")
            return None
        except cls.MultipleObjectsReturned as e:
            # データの整合性エラー（1つの年の1つの月に複数の目標が存在する）
            logger.error(f"[MonthGoal] Data integrity issue: Multiple entries found for month_goal_id={month_goal.id}, todo_id={todo_id}. Error: {e}")
            return None
        except DatabaseError as e:
            # データベース関連のエラー
            logger.error(f"[MonthGoal] DatabaseError: month_goal_id={month_goal.id}, todo_id={todo_id}. Error: {e}")
            return None
        except Exception as e:
            # 予期しないエラーのキャッチ
            logger.exception(f"[MonthGoal] Unexpected error: month_goal_id={month_goal.id}, todo_id={todo_id}. Error: {e}")
            return None

    def mark_as_achieved(self):
        """
        Todoを達成済みに変更する
        Raises:
            Exception: データベースの保存に失敗した場合
        """
        try:
            self.status = self.STATUS_ACHIEVED
            self.save()
            logger.info(f"[Todo] ID:{self.id} marked as achieved.")
        except Exception as e:
            logger.error(f"[Todo] Failed to mark Todo ID:{self.id} as achieved. Error: {e}")
            raise
