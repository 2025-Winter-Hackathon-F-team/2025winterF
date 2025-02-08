import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# .envファイルを読み込む
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "fapp",
    "account",
    "goal"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "fproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "fproject.wsgi.application"

# カスタムユーザーモデルとして 'account.User' を使用する設定
# Django のデフォルトの User モデルの代わりに、このモデルが認証システムで使用されます。
AUTH_USER_MODEL = "account.User"

# ログイン後リダイレクトするURL名を指定
LOGIN_REDIRECT_URL = "goal:home"

# ログアウト後リダイレクトするURL名を指定
LOGOUT_REDIRECT_URL = "account:login"

# ログインページのURL名を指定
LOGIN_URL = "account:login"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        # 利用するデータベースの種類を記載
        "ENGINE": "django.db.backends.mysql",
        # mysql上のデータベースを選択
        "NAME": "fteam_db",
        # mysql上のユーザーを選択
        "USER": "fteam_user",
        # 上記ユーザーのパスワードを記載
        "PASSWORD": "fteam_pass",
        # データベースのホスト名を記載（docker-composeで作成した場合、コンテナ名でアクセスできる）
        "HOST": "db",
        # 対象サーバー（コンテナ）のポート番号を記載
        "PORT": "3306",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"

# エラー解消のために記述。
# デプロイ時に静的ファイルが集約されるディレクトリ
# STATIC_ROOT = "/usr/src/app/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# 開発時ここにある静的ファイルを、デプロイ時STATIC_ROOTに集約する
STATICFILES_DIRS = [BASE_DIR / "static"]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ログの設定（開発用）
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
