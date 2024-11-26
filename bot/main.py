from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from bot.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def send_welcome(message: Message):
    await message.reply("Привет! Я твой To-Do бот. Напиши /help, чтобы узнать, что я умею.")

# Основной запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)