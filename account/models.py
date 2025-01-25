from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password):
        """
        ユーザーを作成するためのメソッド。
        Args:
            email (str): ユーザーのメールアドレス。
            password (str): ユーザーのパスワード。
        Returns:
            user: 作成されたユーザーオブジェクト。
        Raises:
            ValidationError: パスワードの強度が不十分な場合。
            IntegrityError: 同じメールアドレスを持つユーザーが既に存在する場合。
        """
        # パスワードの強度チェック
        validate_password(password)
        # メールアドレスの正規化
        email = self.normalize_email(email)
        # ユーザーを作成
        user = self.model(email=email)
        user.set_password(password)
        try:
            user.save(using=self._db)
        except IntegrityError:
            raise IntegrityError("このメールアドレスはすでに登録されています。")
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True, null=False)
    name = models.CharField(max_length=64, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    deathday = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # フィールドを無効化
    last_login = None

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table="users"

    def __str__(self):
        return self.email