from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, CustomLoginView, CustomUserView, user_block, CustomUserDetail, CustomUserUpdate

app_name = UsersConfig.name

urlpatterns = [
    path("login/", CustomLoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="web_mailing:clients_list"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("users_list/", CustomUserView.as_view(), name="users_list"),
    path("user_block/<int:pk>", user_block, name="user_block"),
    path("user_detail/<int:pk>", CustomUserDetail.as_view(), name="user_detail"),
    path("user_update/<int:pk>", CustomUserUpdate.as_view(), name="user_update")
]
