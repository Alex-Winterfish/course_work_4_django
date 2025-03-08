# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = "add group admin_products"

    def handle(self, *args, **kwargs):

        user = CustomUser.objects.get(email="manager_1@gmail.com")
        group, created = Group.objects.get_or_create(name='managers')
        user.groups.add(group)
        self.stdout.write(self.style.SUCCESS(f'Пользователь {user.username} добавлен в группу admin_products.'))