import asyncpg
from config import DB_CONFIG

#MARK: Функция для создания пула подключений к базе данных.
async def create_db_pool():
    return await asyncpg.create_pool(
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["dbname"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"]
    )

# Функция для проверки соединения с базой данных.
async def check_connection(pool):
    try:
        async with pool.acquire() as connection:
            result = await connection.fetch('SELECT 1')
            print("Подключение к базе данных успешно!")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")

async def create_tables(pool):
    async with pool.acquire() as connection:
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                task TEXT NOT NULL,
                done BOOLEAN DEFAULT FALSE
            )
        """)

#добавление таска
async def add_task(pool, user_id: int, task: str):
    async with pool.acquire() as connection:
        await connection.execute("""
            INSERT INTO tasks (user_id, task) VALUES ($1, $2)
        """, user_id, task)
