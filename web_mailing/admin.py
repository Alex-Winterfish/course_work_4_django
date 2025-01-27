from django.contrib import admin
from .models import MessageModel, ClientModel, MailingModel, MailingAttemptModel

@admin.register(ClientModel)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email")
    list_filter = ["full_name"]
    search_fields = ["full_name", "email"]

@admin.register(MessageModel)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("title", "text")
    list_filter = ["title"]
    search_fields = ["title"]

@admin.register(MailingModel)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("start", "end", "status")
    list_filter = ["message", "recipients"]
    search_fields = ["status"]

@admin.register(MailingAttemptModel)
class Attempt(admin.ModelAdmin):
    list_display = ("attempt_start", "status")
    list_filter = ["status"]
    search_fields = ["status"]