import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "8679809165:AAEoIzOIuFMTtm-43WrRdhgO-lntAEu03QQ")

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logger.info(f"Токен: {BOT_TOKEN[:20]}...")

# База фильмов (100)
MOVIES_DB = [
    {"title": "Побег из Шоушенка", "year": "1994", "rating": "9.3", "genre": "Драма", "country": "США", "duration": "142 мин", "description": "Бухгалтер обвинён в убийстве жены. В тюрьме он находит друзей.", "player_url": "https://rutube.ru/video/search/побег+из+шоушенка"},
    {"title": "Зелёная миля", "year": "1999", "rating": "9.2", "genre": "Драма", "country": "США", "duration": "189 мин", "description": "Начальник блока смертников встречает заключённого с даром.", "player_url": "https://rutube.ru/video/search/зелёная+миля"},
    {"title": "Крёстный отец", "year": "1972", "rating": "9.2", "genre": "Криминал", "country": "США", "duration": "175 мин", "description": "Сага о мафиозной семье Корлеоне.", "player_url": "https://rutube.ru/video/search/крёстный+отец"},
    {"title": "Тёмный рыцарь", "year": "2008", "rating": "9.0", "genre": "Боевик", "country": "США", "duration": "152 мин", "description": "Бэтмен противостоит Джокеру.", "player_url": "https://rutube.ru/video/search/тёмный+рыцарь"},
    {"title": "1+1 (Неприкасаемые)", "year": "2011", "rating": "8.9", "genre": "Комедия", "country": "Франция", "duration": "112 мин", "description": "Аристократ и парень с улицы становятся друзьями.", "player_url": "https://rutube.ru/video/search/1+1+неприкасаемые"},
    {"title": "Матрица", "year": "1999", "rating": "8.7", "genre": "Фантастика", "country": "США", "duration": "136 мин", "description": "Хакер узнаёт, что мир — симуляция.", "player_url": "https://rutube.ru/video/search/матрица"},
    {"title": "Интерстеллар", "year": "2014", "rating": "8.7", "genre": "Фантастика", "country": "США", "duration": "169 мин", "description": "Экспедиция через червоточину.", "player_url": "https://rutube.ru/video/search/интерстеллар"},
    {"title": "Начало", "year": "2010", "rating": "8.8", "genre": "Фантастика", "country": "США", "duration": "148 мин", "description": "Вор крадёт секреты из снов.", "player_url": "https://rutube.ru/video/search/начало+2010"},
    {"title": "Форрест Гамп", "year": "1994", "rating": "8.8", "genre": "Драма", "country": "США", "duration": "142 мин", "description": "Простой парень становится участником великих событий.", "player_url": "https://rutube.ru/video/search/форрест+гамп"},
    {"title": "Бойцовский клуб", "year": "1999", "rating": "8.8", "genre": "Драма", "country": "США", "duration": "139 мин", "description": "Клерк создаёт подпольный бойцовский клуб.", "player_url": "https://rutube.ru/video/search/бойцовский+клуб"},
]

# Главная клавиатура
def get_keyboard():
    kb = [
        [KeyboardButton(text="🎬 Все фильмы"), KeyboardButton(text="🔍 Поиск")],
        [KeyboardButton(text="🎲 Случайный"), KeyboardButton(text="📊 Топ")],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# Клавиатура для фильма
def get_movie_kb(url):
    kb = [[InlineKeyboardButton(text="▶️ Смотреть", url=url)]]
    return InlineKeyboardMarkup(inline_keyboard=kb)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(f"Получена команда /start от {message.from_user.id}")
    try:
        await message.answer(
            "🎬 <b>Бот «Что посмотреть?»</b>\n\n"
            f"📚 <b>{len(MOVIES_DB)}</b> фильмов бесплатно!\n\n"
            "Выберите действие:",
            parse_mode="HTML",
            reply_markup=get_keyboard()
        )
        logger.info("Ответ на /start отправлен")
    except Exception as e:
        logger.error(f"Ошибка при ответе на /start: {e}")

# Кнопка "Все фильмы"
@dp.message(F.text == "🎬 Все фильмы")
async def all_movies(message: Message):
    text = "📋 <b>Все фильмы:</b>\n\n"
    for i, m in enumerate(MOVIES_DB, 1):
        text += f"{i}. {m['title']} ({m['year']}) ⭐{m['rating']}\n"
    await message.answer(text, parse_mode="HTML")

# Кнопка "Поиск"
@dp.message(F.text == "🔍 Поиск")
async def search_cmd(message: Message):
    await message.answer("🔍 Введите название фильма:", reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️ Назад")]], resize_keyboard=True))

# Кнопка "Случайный"
@dp.message(F.text == "🎲 Случайный")
async def random_movie(message: Message):
    import random
    m = random.choice(MOVIES_DB)
    text = f"🎲 <b>{m['title']}</b>\n⭐ {m['rating']} | {m['year']}\n{m['description']}"
    await message.answer(text, parse_mode="HTML", reply_markup=get_movie_kb(m['player_url']))

# Кнопка "Топ"
@dp.message(F.text == "📊 Топ")
async def top_movies(message: Message):
    top = sorted(MOVIES_DB, key=lambda x: float(x['rating']), reverse=True)[:5]
    text = "📊 <b>Топ-5:</b>\n\n"
    for i, m in enumerate(top, 1):
        text += f"{i}. {m['title']} — ⭐{m['rating']}\n"
    await message.answer(text, parse_mode="HTML")

# Кнопка "Назад"
@dp.message(F.text == "⬅️ Назад")
async def back(message: Message):
    await cmd_start(message)

# Текстовый поиск
@dp.message()
async def text_search(message: Message):
    query = message.text.lower()
    found = [m for m in MOVIES_DB if query in m['title'].lower()]
    if found:
        for m in found[:3]:
            text = f"🎬 <b>{m['title']}</b>\n⭐ {m['rating']} | {m['year']}\n{m['description']}"
            await message.answer(text, parse_mode="HTML", reply_markup=get_movie_kb(m['player_url']))
    else:
        await message.answer(f"😔 \"{message.text}\" не найден")

async def main():
    logger.info("🚀 Запуск бота...")
    logger.info(f"Фильмов: {len(MOVIES_DB)}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
