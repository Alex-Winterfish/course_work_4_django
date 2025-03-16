# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = "add group managers"

    def handle(self, *args, **kwargs):

        user = CustomUser.objects.get(email="manager_1@gmail.com")
        group, created = Group.objects.get_or_create(name="managers")
        client_view_permission = Permission.objects.get(codename="can_view_client")
        message_view_permission = Permission.objects.get(codename="can_view_message")
        mailing_view_permission = Permission.objects.get(codename="can_view_mailing")
        disable_permission = Permission.objects.get(codename="can_disable_mailing")
        block_permission = Permission.objects.get(codename="can_block_user")
        group.permissions.add(
            client_view_permission,
            mailing_view_permission,
            message_view_permission,
            disable_permission,
            block_permission,
        )
        user.groups.add(group)
        self.stdout.write(
            self.style.SUCCESS(
                f"Пользователь {user.username} добавлен в группу managers."
            )
        )
