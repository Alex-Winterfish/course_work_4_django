from django.contrib import admin
from .models import MessageModel, ClientModel

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