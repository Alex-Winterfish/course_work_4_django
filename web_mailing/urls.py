from django.urls import path
from web_mailing.apps import WebMailingConfig
from .views import ClientView, ClientCreate, ClientDetail, ClientUpdate

app_name = WebMailingConfig.name

urlpatterns = [
    path("clients/", ClientView.as_view(), name="web_mailing")
]