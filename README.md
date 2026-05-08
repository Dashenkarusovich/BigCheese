# Big Cheese Languages — Telegram Bot Production Package

Финальная версия для переноса на контур Дарьи.

## Что делает бот

- RU/EN стартовый сценарий
- Отправляет PDF
- Сегментирует пользователя: relocation / career / other
- Отправляет ежедневную 4-дневную цепочку после выбора сегмента
- При заявке отправляет уведомление Дарье в Telegram
- При заявке отправляет данные в Google Sheets / Dashboard через Apps Script Web App

## Railway Variables

Обязательные:

```
BOT_TOKEN=новый_токен_от_BotFather
ADMIN_CHAT_ID=1175970327
TEST_MODE=0
SHEET_WEBHOOK_URL=https://script.google.com/macros/s/.../exec
```

Для теста можно поставить `TEST_MODE=1`: сообщения уйдут через 2/4/6/7 минут.
Для production обязательно `TEST_MODE=0`: сообщения уходят через 24/48/72/96 часов.

## Start Command

```
python bot.py
```

## Root Directory

Пустой. Все файлы лежат в корне репозитория.

## Финальный канал

https://t.me/BigCheesemaster

## Важно перед запуском

1. Дарья должна открыть бота и нажать `/start`, чтобы бот мог отправлять ей уведомления.
2. После переноса перевыпустить bot token в BotFather.
3. Не хранить токены в GitHub.
4. Проверить путь: бот → заявка Дарье → Google Sheets / Dashboard.
