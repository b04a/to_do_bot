from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F
import asyncio
from config import BOT_TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хэндлер команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я твой To-Do бот. Напиши /help, чтобы узнать, что я умею.")

# Основная функция запуска бота
async def main():
    try:
        print("Бот запущен!")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
