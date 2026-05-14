from scheduler import run_scheduler
from config import TELEGRAM_BOT_TOKEN

if not TELEGRAM_BOT_TOKEN:
    print("⚠️ Внимание: TELEGRAM_BOT_TOKEN не настроен в .env файле")
    print("Создайте .env файл с вашим токеном бота")
    exit(1)

if __name__ == "__main__":
    print("Запуск бота автомобильных новостей...")
    run_scheduler()