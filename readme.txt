✔ многопоточность
✔ случайный прокси
✔ случайные задержки
✔ сохранение результатов
✔ устойчивость к ошибкам

Структура проекта:

mail_checker/
│
├ accounts.txt
├ proxies.txt
├ good.txt
├ bad.txt
└ checker.py
1️⃣ Файл аккаунтов

accounts.txt

email1@outlook.com|REFRESH_TOKEN|CLIENT_ID
email2@outlook.com|REFRESH_TOKEN|CLIENT_ID
email3@outlook.com|REFRESH_TOKEN|CLIENT_ID
2️⃣ Файл прокси

proxies.txt

http://user:pass@1.2.3.4:8080
http://user:pass@5.6.7.8:8080
http://user:pass@9.10.11.12:8080
3️⃣ Установка библиотек
pip install requests pysocks

⚡ Что делает этот скрипт

Он:

1️⃣ загружает аккаунты
2️⃣ загружает прокси
3️⃣ запускает 10 потоков
4️⃣ каждому аккаунту даёт случайный прокси
5️⃣ получает OAuth токен
6️⃣ подключается к IMAP
7️⃣ читает последние письма

📂 Результаты

Файлы:

good.txt

рабочие аккаунты

bad.txt

ошибки / невалидные

🔒 Безопасные настройки

Рекомендую:

threads = 5-15

Иначе Outlook может:

начать rate limit

требовать дополнительную проверку