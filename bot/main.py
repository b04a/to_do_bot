from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import BOT_TOKEN
from db import create_db_pool, create_tables, check_connection, add_task, get_tasks
import asyncio

# Создаём объект бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаём пул подключений и таблицы при старте бота
async def on_startup():
    pool = await create_db_pool()
    await create_tables(pool)
    await check_connection(pool)  # Проверяем соединение с БД
    return pool

# Передаем пул в диспетчер как атрибут
dp.pool = None

# Хэндлер команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я твой To-Do бот. Напиши /help, чтобы узнать, что я умею.")

# Хэндлер команды /help
@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("/add <task> - добавить задачу\n"
                         "/list - показать все задачи\n"
                         "/done <task_id> - пометить задачу как выполненную\n"
                         "/delete <task_id> - удалить задачу")

# Хэндлер команды /add
@dp.message(Command("add"))
async def add(message: Message):
    task = message.text[len("/add "):].strip()
    if task:
        # Передаем пул из диспетчера в функцию
        await add_task(dp.pool, message.from_user.id, task)
        await message.answer(f"Задача '{task}' добавлена!")
    else:
        await message.answer("Пожалуйста, укажи текст задачи после команды.")

@dp.message(Command("list"))
async def list_tasks(message: Message):
    tasks = await get_tasks(dp.pool, message.from_user.id)
    if tasks:
        task_list = "\n".join([f"{task['id']}. {task['task']} - {'Выполнено' if task['done'] else 'Не выполнено'}"
                             for task in tasks])
        await message.answer(f"Ваши задачи:\n{task_list}")
    else:
        await message.answer("У вас нет задач.")

async def main():
    # Инициализируем пул и передаем его в диспетчер
    dp.pool = await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
