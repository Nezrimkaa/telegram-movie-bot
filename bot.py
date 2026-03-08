import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

# Токен бота от @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "6907852914:AAEElYjSSP5KuxPl4lrucI5kT2ihES3lkRw")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 🔥 ГОТОВАЯ БАЗА ФИЛЬМОВ С ПЛЕЕРАМИ 🔥
# Ссылки на YouTube с фильмами (трейлеры + полные фильмы)
MOVIES_DB = [
    {
        "title": "Побег из Шоушенка",
        "year": "1994",
        "rating": "9.3",
        "genre": "Драма",
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника.",
        "player_url": "https://www.youtube.com/embed/NmzuHjWmXOc"
    },
    {
        "title": "Зелёная миля",
        "year": "1999",
        "rating": "9.2",
        "genre": "Драма / Фэнтези",
        "description": "Пол Эджкомб — начальник блока смертников в тюрьме.",
        "player_url": "https://www.youtube.com/embed/Kt9IM0x-0F0"
    },
    {
        "title": "1+1 (Неприкасаемые)",
        "year": "2011",
        "rating": "8.9",
        "genre": "Комедия / Драма",
        "description": "Аристократ в инвалидном кресле нанимает в сиделки парня с криминальным прошлым.",
        "player_url": "https://www.youtube.com/embed/34XTzDzjzQo"
    },
    {
        "title": "Интерстеллар",
        "year": "2014",
        "rating": "8.7",
        "genre": "Фантастика",
        "description": "Группа исследователей отправляется в червоточину в поисках нового дома для человечества.",
        "player_url": "https://www.youtube.com/embed/zSWdZVtXT7E"
    },
    {
        "title": "Начало",
        "year": "2010",
        "rating": "8.8",
        "genre": "Боевик / Фантастика",
        "description": "Кобб — талантливый вор, который крадёт секреты из подсознания во время сна.",
        "player_url": "https://www.youtube.com/embed/YoHD9XEInc0"
    },
    {
        "title": "Матрица",
        "year": "1999",
        "rating": "8.7",
        "genre": "Боевик / Фантастика",
        "description": "Хакер Нео узнаёт, что наш мир — это симуляция, созданная машинами.",
        "player_url": "https://www.youtube.com/embed/vKQi3bBA1y8"
    },
    {
        "title": "Тёмный рыцарь",
        "year": "2008",
        "rating": "9.0",
        "genre": "Боевик / Драма",
        "description": "Бэтмен сражается с Джокером — гениальным преступником, сеющим хаос в Готэме.",
        "player_url": "https://www.youtube.com/embed/EXeTwQWrcwY"
    },
    {
        "title": "Крёстный отец",
        "year": "1972",
        "rating": "9.2",
        "genre": "Криминал / Драма",
        "description": "История мафиозной семьи Корлеоне и её главы Вито Корлеоне.",
        "player_url": "https://www.youtube.com/embed/sY1S34973zA"
    },
    {
        "title": "Властелин колец: Братство Кольца",
        "year": "2001",
        "rating": "8.8",
        "genre": "Фэнтези",
        "description": "Фродо Бэггинс отправляется в опасное путешествие, чтобы уничтожить Кольцо Всевластия.",
        "player_url": "https://www.youtube.com/embed/V75dMMIW2B4"
    },
    {
        "title": "Форрест Гамп",
        "year": "1994",
        "rating": "8.8",
        "genre": "Драма / Комедия",
        "description": "История простого парня с большим сердцем, который становится свидетелем важных событий.",
        "player_url": "https://www.youtube.com/embed/bLvqoHBptjg"
    },
    {
        "title": "Бойцовский клуб",
        "year": "1999",
        "rating": "8.8",
        "genre": "Драма / Триллер",
        "description": "Скучающий клерк создаёт подпольный бойцовский клуб, который становится чем-то большим.",
        "player_url": "https://www.youtube.com/embed/SUXWAEX2jlg"
    },
    {
        "title": "Гарри Поттер и философский камень",
        "year": "2001",
        "rating": "7.6",
        "genre": "Фэнтези / Приключения",
        "description": "Мальчик-сирота узнаёт, что он волшебник, и отправляется в школу магии Хогвартс.",
        "player_url": "https://www.youtube.com/embed/Lny4vVLfJ-E"
    },
    {
        "title": "Мстители: Война бесконечности",
        "year": "2018",
        "rating": "8.4",
        "genre": "Боевик / Фантастика",
        "description": "Мстители объединяются, чтобы остановить Таноса и спасти вселенную.",
        "player_url": "https://www.youtube.com/embed/6ZfuNTqbHE8"
    },
    {
        "title": "Титаник",
        "year": "1997",
        "rating": "7.9",
        "genre": "Драма / Мелодрама",
        "description": "История любви между аристократкой и бедным художником на борту Титаника.",
        "player_url": "https://www.youtube.com/embed/kVrqfYjkTdQ"
    },
    {
        "title": "Джокер",
        "year": "2019",
        "rating": "8.4",
        "genre": "Триллер / Драма",
        "description": "История происхождения главного врага Бэтмена — клоуна-преступника Джокера.",
        "player_url": "https://www.youtube.com/embed/zAGVQLHvwOY"
    }
]


def create_movie_keyboard(movie: dict) -> InlineKeyboardMarkup:
    """Создание клавиатуры для фильма с кнопкой просмотра"""
    keyboard = []
    
    # Кнопка "Смотреть" с WebApp для встроенного плеера
    keyboard.append([
        InlineKeyboardButton(
            text="🎬 Смотреть онлайн",
            web_app=WebAppInfo(url=movie.get('player_url', 'https://youtube.com'))
        )
    ])
    
    # Кнопка поиска на YouTube
    search_url = f"https://www.youtube.com/results?search_query={movie['title'].replace(' ', '+')}+смотреть+онлайн"
    keyboard.append([
        InlineKeyboardButton(
            text="🔍 Найти на YouTube",
            url=search_url
        )
    ])
    
    # Кнопка с информацией о фильме
    keyboard.append([
        InlineKeyboardButton(
            text="ℹ️ О фильме",
            callback_data=f"movie_info_{movie['title']}"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_movies_list_keyboard(movies: list) -> InlineKeyboardMarkup:
    """Клавиатура со списком фильмов для навигации"""
    keyboard = []
    
    for i in range(0, len(movies), 2):
        row = []
        row.append(InlineKeyboardButton(
            text=f"🎬 {movies[i]['title'][:20]}...",
            callback_data=f"show_movie_{i}"
        ))
        if i + 1 < len(movies):
            row.append(InlineKeyboardButton(
                text=f"🎬 {movies[i+1]['title'][:20]}...",
                callback_data=f"show_movie_{i+1}"
            ))
        keyboard.append(row)
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    await message.answer(
        f"🎬 <b>Добро пожаловать в бот «Что посмотреть?»!</b>\n\n"
        f"Я помогу вам выбрать фильм для просмотра. В моей базе уже есть <b>{len(MOVIES_DB)}</b> лучших фильмов!\n\n"
        f"<b>Команды:</b>\n"
        f"📋 /movies — показать все фильмы\n"
        f"🔍 /search — поиск фильма\n"
        f"🎲 /random — случайный фильм\n"
        f"📊 /top — топ фильмов по рейтингу\n\n"
        f"Нажмите кнопку ниже, чтобы выбрать фильм, или введите название для поиска! 🍿",
        parse_mode="HTML",
        reply_markup=create_movies_list_keyboard(MOVIES_DB[:10])
    )


@dp.message(Command("movies"))
async def cmd_movies(message: types.Message):
    """Обработчик команды /movies - показывает список фильмов"""
    await message.answer(
        f"📋 <b>Все фильмы в базе ({len(MOVIES_DB)}):</b>\n\n"
        f"Выберите фильм из списка:",
        parse_mode="HTML",
        reply_markup=create_movies_list_keyboard(MOVIES_DB)
    )


@dp.callback_query(lambda c: c.data.startswith("show_movie_"))
async def callback_show_movie(callback: types.CallbackQuery):
    """Показ информации о фильме по индексу"""
    try:
        index = int(callback.data.split("_")[-1])
        movie = MOVIES_DB[index]
        
        text = (
            f"🎬 <b>{movie['title']}</b>\n\n"
            f"📅 Год: {movie['year']}\n"
            f"⭐ Рейтинг: {movie['rating']}\n"
            f"🎭 Жанр: {movie['genre']}\n\n"
            f"📝 <i>{movie['description']}</i>"
        )
        
        await callback.message.answer(
            text,
            parse_mode="HTML",
            reply_markup=create_movie_keyboard(movie)
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка в callback_show_movie: {e}")
        await callback.answer("Ошибка при загрузке фильма", show_alert=True)


@dp.callback_query(lambda c: c.data.startswith("movie_info_"))
async def callback_movie_info(callback: types.CallbackQuery):
    """Показ подробной информации о фильме"""
    title = callback.data.replace("movie_info_", "")
    movie = next((m for m in MOVIES_DB if m['title'] == title), None)
    
    if movie:
        text = (
            f"🎬 <b>{movie['title']}</b>\n\n"
            f"📅 Год выпуска: {movie['year']}\n"
            f"⭐ Рейтинг IMDb: {movie['rating']}\n"
            f"🎭 Жанр: {movie['genre']}\n\n"
            f"📝 <b>Описание:</b>\n"
            f"<i>{movie['description']}</i>\n\n"
            f"🎥 Нажмите «Смотреть онлайн» для просмотра!"
        )
        
        await callback.message.answer(
            text,
            parse_mode="HTML",
            reply_markup=create_movie_keyboard(movie)
        )
    
    await callback.answer()


@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    """Обработчик команды /search - поиск фильма"""
    await message.answer(
        "🔍 <b>Поиск фильма</b>\n\n"
        "Введите название фильма для поиска:\n\n"
        f"<i>Доступно фильмов в базе: {len(MOVIES_DB)}</i>",
        parse_mode="HTML"
    )


@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    """Случайный фильм"""
    import random
    movie = random.choice(MOVIES_DB)
    
    text = (
        f"🎲 <b>Случайный выбор:</b>\n\n"
        f"🎬 <b>{movie['title']}</b>\n"
        f"📅 Год: {movie['year']}\n"
        f"⭐ Рейтинг: {movie['rating']}\n"
        f"🎭 Жанр: {movie['genre']}\n\n"
        f"📝 <i>{movie['description']}</i>"
    )
    
    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=create_movie_keyboard(movie)
    )


@dp.message(Command("top"))
async def cmd_top(message: types.Message):
    """Топ фильмов по рейтингу"""
    sorted_movies = sorted(MOVIES_DB, key=lambda x: float(x['rating']), reverse=True)[:5]
    
    text = "📊 <b>Топ-5 фильмов по рейтингу:</b>\n\n"
    for i, movie in enumerate(sorted_movies, 1):
        text += f"{i}. 🎬 <b>{movie['title']}</b> — ⭐ {movie['rating']}\n"
    
    text += "\nНажмите /movies чтобы увидеть все фильмы"
    
    await message.answer(text, parse_mode="HTML")


@dp.message()
async def handle_text(message: types.Message):
    """Обработчик текстовых сообщений - поиск фильма"""
    if message.text.startswith('/'):
        return
    
    search_query = message.text.lower()
    await message.answer(f"🔍 Ищу: <b>{message.text}</b>...", parse_mode="HTML")
    
    # Поиск в базе
    found_movies = [m for m in MOVIES_DB if search_query in m['title'].lower()]
    
    if found_movies:
        for movie in found_movies[:5]:
            text = (
                f"🎬 <b>{movie['title']}</b>\n"
                f"📅 Год: {movie['year']} | ⭐ {movie['rating']}\n"
                f"🎭 Жанр: {movie['genre']}\n\n"
                f"<i>{movie['description']}</i>"
            )
            await message.answer(
                text,
                parse_mode="HTML",
                reply_markup=create_movie_keyboard(movie)
            )
    else:
        # Если не найдено, предлагаем посмотреть на YouTube
        text = (
            f"😔 <b>{message.text}</b> не найден в базе.\n\n"
            f"Но вы можете посмотреть его на YouTube:"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🔍 Найти на YouTube",
                url=f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}+смотреть+онлайн"
            )]
        ])
        
        await message.answer(
            text,
            parse_mode="HTML",
            reply_markup=keyboard
        )


async def main():
    """Запуск бота"""
    logger.info(f"🚀 Запуск бота «Что посмотреть?»...")
    logger.info(f"📊 Загружено фильмов: {len(MOVIES_DB)}")
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
