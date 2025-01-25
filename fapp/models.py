# models.pyはデータベースの動きを記述する。
# ユーザーの登録の処理もここに書く。
from datetime import datetime
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# user作成のメソッド
class CustomUserManager(BaseUserManager):
    # ユーザー作成のメソッド。
    def create_user(self, email, name, password):
        # emailの入力がなかった場合の処理
        if not email:
            raise ValueError("メールアドレスを入力してください")
        #新しいユーザーモデルのインスタンスを作成
        user = self.model(
            # emailを正規化して保存
            email = self.normalize_email(email),
            # 名前保存
            name = name,   
        )
        # パスワードをハッシュ化し、ユーザーp部ジェクトのpasswordフィールドに保存
        user.set_password(password)
        # ユーザーオブジェクトのDBへの保存
        user.save(using=self._db)
        # 作成されたユーザーオブジェクトを返す
        return user
# superuser作成のメソッド
    def create_superuser(self, email, name, password):
        #スタッフ権限、スーパーユーザー権限を与える 
        user = self.create_user(
            email = email,
            name = name,
            password = password
        )
        user.is_staff = True
        user.is_superuser = True
        # データベースに保存
        user.save(using=self._db)
        return user

# Usersテーブルの作成
# passwordフィールドは組み込まれている
class Users(AbstractBaseUser, PermissionsMixin):
    # email VACHAR(255) NOT NULL UNIQUE
    email = models.EmailField(unique = True, max_length=254, verbose_name="メールアドレス")
    # name VACHAR(64)
    name = models.CharField(max_length=64, verbose_name="ユーザーネーム")
    # birthday DATE、null=TrueにしてデータベースでのnullはOKに。blank=Trueにはしない。フォームで入力省略にはしない
    birthday = models.DateField(verbose_name="誕生日", null=True)
    # deathday DATE
    dethday = models.DateField(verbose_name="想定寿命", null=True)
    # created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now=True)
    # update_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    updated_at = models.DateField(auto_now_add=True)
    # スーパーユーザーのフィールド
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # emailをログインIDとして使用。
    USERNAME_FIELD = "email"
    # スーパーユーザーを作成する際に必要になる項目。manage.pycreateuserコマンドで入力を求められる
    REQUIRED_FIELDS = ["name"]
    # CustomUserManagerでユーザーモデルをカスタマイズしたので設定。create_user,create_superuserメソッドを通してユーザーオブジェクトが作成可能。
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.name} ({self.email})"

# YearGoalsテーブルの作成
class YearGoals(models.Model):
    # statusでTINYINTを実現するための記述
    STATUS_CHOICES = [
        (0, "未達"),
        (1, "達成")
    ]
    # FK:user_id INT NOT NULL 
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    # year DATE NOT NULL datetimeモジュールを使用して年のみを追加する PositiveSmallは小さい数字が入る
    year = models.PositiveSmallIntegerField(default=datetime.now().year)
    # title VACHAR(50) NOT NULL
    title = models.CharField(max_length=50, verbose_name="年間目標を入力してください")
    # status TYNTINT DEFAULT 0 NOT NULL
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    # created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now=True)
    # update_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    updated_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.year} - {self.title} ({self.user.email})"


# MonthGoalsテーブルの作成
class MonthGoals(models.Model):
    STATUS_CHOICES = [
        (0, "未達"),
        (1, "達成")
    ]
    # FK:year_goal_id INT NOT NULL
    year_goal = models.ForeignKey(YearGoals, on_delete=models.CASCADE) 
    # month DATE NOT NULL
    month = models.PositiveSmallIntegerField(default=datetime.now().year)
    # title VACHAR(50) NOT NULL
    title = models.CharField(max_length=50, verbose_name="月の目標を入力してください")
    # status TYNTINT DEFAULT 0 NOT NULL
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    # created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now=True)
    # update_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    updated_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.year_goal.title} - {self.title} ({self.month}月)"

# Todosテーブルの作成
class Todos(models.Model):
    STATUS_CHOICES = [
        (0, "未達"),
        (1, "達成")
    ]
    # FK:month_goal_id INT NOT NULL 
    month_goal = models.ForeignKey(MonthGoals, on_delete=models.CASCADE) 
    # title VACHAR(50) NOT NULL
    title = models.CharField(max_length=50, verbose_name="日々のタスクを入力してください")
    # status TYNTINT DEFAULT 0 NOT NULL
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    # created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now=True)
    # update_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    updated_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.month_goal.title} - {self.title}"

# MessagesMSTテーブルの作成
class MessageMST(models.Model):
    TYPE_CHOICES = [
        (0, "お叱り"),
        (1, "お褒め")
    ]
    # message TEXT NOT NULL
    message = models.TextField() 
    # status TYNTINT DEFAULT 0 NOT NULL
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    # created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now=True)
    # update_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    updated_at = models.DateField(auto_now_add=True)
    