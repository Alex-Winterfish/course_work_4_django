from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig
from .views import RegisterView, CustomLoginView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", CustomLoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="web_mailing:clients_list"), name="logout"),
    path("register/", RegisterView.as_view(), name="register")
]
