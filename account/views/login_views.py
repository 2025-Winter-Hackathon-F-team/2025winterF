from django.contrib.auth.views import LoginView

from ..forms import LoginForm

class LoginView(LoginView):
    template_name = "login.html"
    form_class = LoginForm