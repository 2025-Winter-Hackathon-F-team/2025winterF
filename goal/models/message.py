import logging

from django.db import models, DatabaseError


logger = logging.getLogger(__name__)


class Message(models.Model):
    # メッセージタイプを表す定数
    MESSAGE_TYPE_SCOLD = 0
    MESSAGE_TYPE_PRAISE = 1

    # message_typeフィールドの選択肢 (DB保存値, 表示文字列)
    TYPE_CHOICES = [
        (MESSAGE_TYPE_SCOLD, "お叱り"),
        (MESSAGE_TYPE_PRAISE, "お褒め"),
    ]

    # message TEXT NOT NULL
    message = models.TextField(verbose_name="メッセージ内容")
    # message_type PositiveSmallIntegerField NOT NULL
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, verbose_name="メッセージタイプ")
    # created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    # updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        db_table="messages"
        verbose_name="メッセージ"
        verbose_name_plural = "メッセージ一覧"

    def __str__(self):
        return self.message

    @classmethod
    def get_praise_messages(cls):
        """
        お褒めの言葉の一覧を取得する

        Returns:
            QuerySet(Message): お褒めの言葉一覧 (エラー時は空の QuerySet)
        """
        try:
            return cls.objects.filter(type=cls.MESSAGE_TYPE_PRAISE)
        except DatabaseError as e:
            logger.error(
                f"Database error when fetching praise messages: {e}"
            )
        except Exception as e:
            logger.exception(
                f"Unexpected error when fetching praise messages: {e}"
            )
        return cls.objects.none()