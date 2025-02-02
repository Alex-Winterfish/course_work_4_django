from django.urls import path
from web_mailing.apps import WebMailingConfig
from .views import (ClientView, ClientCreate, ClientDetail, ClientUpdate, ClientDelite,
                    MessageView, MessageDetail, MessageCreate, MessageUpdate, MessageDelete, MailingView)

app_name = WebMailingConfig.name

urlpatterns = [
    path("clients/", ClientView.as_view(), name="clients_list"),
    path("client_detail/<int:pk>", ClientDetail.as_view(), name="client_detail"),
    path('client_update/<int:pk>', ClientUpdate.as_view(), name="client_update"),
    path('client_delete/<int:pk>', ClientDelite.as_view(), name="client_delete"),
    path('client_create/', ClientCreate.as_view(), name="client_create"),
    path("messages/", MessageView.as_view(), name="messages_list"),
    path("message_detail/<int:pk>", MessageDetail.as_view(), name="message_detail"),
    path("message_create/", MessageCreate.as_view(), name="message_create"),
    path("message_update/<int:pk>", MessageUpdate.as_view(), name="message_update"),
    path("message_delete/<int:pk>", MessageDelete.as_view(), name="message_delete"),
    path("mailing/", MailingView.as_view(), name="mailing_list")
]