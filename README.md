Перейменовуємо .env.example в .env
Вставляємо дані телеграм, які беремо https://my.telegram.org, under API Development
І вставляємо ID гугл таблиці це 'XYZXYZYXZ' з УРЛа https://docs.google.com/spreadsheets/d/XYZXYZYXZ/edit#gid=2096019021
І називаємо лист в таблиці або "Phone numbers", або змінюємо в .env файлі

Групи для парсингу підібрати самостійно, і занести їх в список tg_groups окремим рядком (лише назва групи).

Далі запускаємо файл:
python_group_replies.py

