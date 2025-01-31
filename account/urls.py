from django.urls import path
from .views import SignUpView, LoginView, SetupView, ProfileView
from django.contrib.auth.views import LogoutView


# 名前空間を設定
app_name = "account"
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("setup/", SetupView.as_view(), name="setup"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
