# Auto News Bot for Telegram

Бот для автоматического сбора и публикации автомобильных новостей в Telegram канал.

## Настройка

1. Клонируйте репозиторий на PythonAnywhere
2. Создайте файл `.env` с токенами:
```
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHANNEL_ID=@your_channel
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите бота:
```bash
python main.py
```

## Запуск по расписанию

На PythonAnywhere используйте Scheduled Tasks или cron:
```bash
# Каждые 2 часа
0 */2 * * * cd /path/to/auto_news_bot && python main.py
```

## Источники новостей

- motor.ru
- drive.ru
- drom.ru
- kolesa.ru
- и другие автомобильные порталы