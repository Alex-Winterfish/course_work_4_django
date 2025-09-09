# ﻿"Сервис управления рассылками"

1. Установить зависимости:
```
pip install -r /path/to/requirements.txt
```
2. В файле .env.sample указать необходимые переменные окружения
3. Для заполнения базы данных выполнить:

```commandline
python manage.py loaddata users_fixture.json --format json
```
Заполняет БД следующими пользователями:
- Petr@gmail.com - пароль qwer12345678
- Ivan@gmail.com - пароль qwer12345678
- Gosha@gmail.com - пароль qwer12345678
- manager_1@gmail.com - пароль qwer12345678

Для добавления пользователя manager_1@gmail.com в группу "managers"
выполнить команду:
```commandline
python manage.py add_to_group
```
ля заполнения базы данных клиентами выполнить:
```commandline
python manage.py loaddata clients_fixture.json --format json
```
для заполнения базы данных сообщениями выполнить:
```commandline
python manage.py loaddata messages_fixture.json --format json
```
для заполнения базы данных рассылками выполнить:
```commandline
python manage.py loaddata mailings_fixture.json --format json
```
4. Реализованна возможность запуска рассылки из командной строки. Для этого выполнить:
```commandline
python manage.py mailing
```
5. Права пользователей в группе managers:
- Возможность блокирования пользователя. Для этого необходимо зайти в профиль пользователя и нажать кнопу "Заблокровать"
- Отключение рассылок. Для этого перейти в "подробнее" у конкретной рассылки и нажать кнопку "отключить рассылку". Статус рассылки поменяется на "Окончена". Рассылки в статусе "Окончена" не могут быть запущены пользователем
