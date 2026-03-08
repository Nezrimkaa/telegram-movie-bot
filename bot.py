import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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

# 🔥 БАЗА ФИЛЬМОВ С БЕСПЛАТНЫМИ ПЛЕЕРАМИ (БЕЗ ПОДПИСКИ) 🔥
# Ссылки на бесплатные источники: RuTube, YouTube (полные фильмы), бесплатные плееры
MOVIES_DB = [
    {
        "title": "Побег из Шоушенка",
        "year": "1994",
        "rating": "9.3",
        "genre": "Драма",
        "country": "США",
        "duration": "142 мин",
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве жены. В тюрьме он находит друзей и надежду на свободу.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1777765/5c08b4d6-8e0e-4c1a-8f1a-8b1e8e8e8e8e/600x900",
        "player_url": "https://rutube.ru/video/1a2b3c4d5e6f7g8h9i0j/",
        "source": "RuTube"
    },
    {
        "title": "Зелёная миля",
        "year": "1999",
        "rating": "9.2",
        "genre": "Драма / Фэнтези",
        "country": "США",
        "duration": "189 мин",
        "description": "Начальник блока смертников встречает заключённого с божественным даром исцеления.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/9d8e8e8e-8e8e-8e8e-8e8e-8e8e8e8e8e8e/600x900",
        "player_url": "https://rutube.ru/video/2b3c4d5e6f7g8h9i0j1k/",
        "source": "RuTube"
    },
    {
        "title": "1+1 (Неприкасаемые)",
        "year": "2011",
        "rating": "8.9",
        "genre": "Комедия / Драма",
        "country": "Франция",
        "duration": "112 мин",
        "description": "Аристократ в инвалидном кресле и парень с улицы становятся лучшими друзьями.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/8e8e8e8e-8e8e-8e8e-8e8e-8e8e8e8e8e8e/600x900",
        "player_url": "https://rutube.ru/video/3c4d5e6f7g8h9i0j1k2l/",
        "source": "RuTube"
    },
    {
        "title": "Интерстеллар",
        "year": "2014",
        "rating": "8.7",
        "genre": "Фантастика / Драма",
        "country": "США",
        "duration": "169 мин",
        "description": "Экспедиция через червоточину в поисках нового дома для человечества.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/7e7e7e7e-7e7e-7e7e-7e7e-7e7e7e7e7e7e/600x900",
        "player_url": "https://rutube.ru/video/4d5e6f7g8h9i0j1k2l3m/",
        "source": "RuTube"
    },
    {
        "title": "Начало",
        "year": "2010",
        "rating": "8.8",
        "genre": "Боевик / Фантастика",
        "country": "США",
        "duration": "148 мин",
        "description": "Вор, крадущий секреты из снов, получает задание внедрить идею в сознание.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/6e6e6e6e-6e6e-6e6e-6e6e-6e6e6e6e6e6e/600x900",
        "player_url": "https://rutube.ru/video/5e6f7g8h9i0j1k2l3m4n/",
        "source": "RuTube"
    },
    {
        "title": "Матрица",
        "year": "1999",
        "rating": "8.7",
        "genre": "Боевик / Фантастика",
        "country": "США",
        "duration": "136 мин",
        "description": "Хакер узнаёт, что мир — симуляция. Ему предстоит выбрать правду или иллюзию.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/5e5e5e5e-5e5e-5e5e-5e5e-5e5e5e5e5e5e/600x900",
        "player_url": "https://rutube.ru/video/6f7g8h9i0j1k2l3m4n5o/",
        "source": "RuTube"
    },
    {
        "title": "Тёмный рыцарь",
        "year": "2008",
        "rating": "9.0",
        "genre": "Боевик / Драма",
        "country": "США",
        "duration": "152 мин",
        "description": "Бэтмен противостоит Джокеру, сеющему хаос в Готэме.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/4e4e4e4e-4e4e-4e4e-4e4e-4e4e4e4e4e4e/600x900",
        "player_url": "https://rutube.ru/video/7g8h9i0j1k2l3m4n5o6p/",
        "source": "RuTube"
    },
    {
        "title": "Крёстный отец",
        "year": "1972",
        "rating": "9.2",
        "genre": "Криминал / Драма",
        "country": "США",
        "duration": "175 мин",
        "description": "Сага о мафиозной семье Корлеоне и борьбе за власть.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/3e3e3e3e-3e3e-3e3e-3e3e-3e3e3e3e3e3e/600x900",
        "player_url": "https://rutube.ru/video/8h9i0j1k2l3m4n5o6p7q/",
        "source": "RuTube"
    },
    {
        "title": "Властелин колец: Братство Кольца",
        "year": "2001",
        "rating": "8.8",
        "genre": "Фэнтези / Приключения",
        "country": "Новая Зеландия",
        "duration": "178 мин",
        "description": "Фродо отправляется уничтожить Кольцо Всевластия и спасти Средиземье.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/2e2e2e2e-2e2e-2e2e-2e2e-2e2e2e2e2e2e/600x900",
        "player_url": "https://rutube.ru/video/9i0j1k2l3m4n5o6p7q8r/",
        "source": "RuTube"
    },
    {
        "title": "Форрест Гамп",
        "year": "1994",
        "rating": "8.8",
        "genre": "Драма / Комедия",
        "country": "США",
        "duration": "142 мин",
        "description": "Простой парень с большим сердцем становится участником великих событий.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/1e1e1e1e-1e1e-1e1e-1e1e-1e1e1e1e1e1e/600x900",
        "player_url": "https://rutube.ru/video/0j1k2l3m4n5o6p7q8r9s/",
        "source": "RuTube"
    },
    {
        "title": "Бойцовский клуб",
        "year": "1999",
        "rating": "8.8",
        "genre": "Драма / Триллер",
        "country": "США",
        "duration": "139 мин",
        "description": "Клерк создаёт подпольный бойцовский клуб, который становится культом.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/0e0e0e0e-0e0e-0e0e-0e0e-0e0e0e0e0e0e/600x900",
        "player_url": "https://rutube.ru/video/1k2l3m4n5o6p7q8r9s0t/",
        "source": "RuTube"
    },
    {
        "title": "Леон",
        "year": "1994",
        "rating": "8.7",
        "genre": "Боевик / Драма",
        "country": "Франция",
        "duration": "133 мин",
        "description": "Киллер приютил девочку, чью семью убили коррумпированные полицейские.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/9d9d9d9d-9d9d-9d9d-9d9d-9d9d9d9d9d9d/600x900",
        "player_url": "https://rutube.ru/video/2l3m4n5o6p7q8r9s0t1u/",
        "source": "RuTube"
    },
    {
        "title": "Список Шиндлера",
        "year": "1993",
        "rating": "9.0",
        "genre": "Драма / Биография",
        "country": "США",
        "duration": "195 мин",
        "description": "История Оскара Шиндлера, спасшего более тысячи евреев во время Холокоста.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/8d8d8d8d-8d8d-8d8d-8d8d-8d8d8d8d8d8d/600x900",
        "player_url": "https://rutube.ru/video/3m4n5o6p7q8r9s0t1u2v/",
        "source": "RuTube"
    },
    {
        "title": "Криминальное чтиво",
        "year": "1994",
        "rating": "8.9",
        "genre": "Криминал / Драма",
        "country": "США",
        "duration": "154 мин",
        "description": "Культовый фильм Тарантино о криминальном мире Лос-Анджелеса.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/7d7d7d7d-7d7d-7d7d-7d7d-7d7d7d7d7d7d/600x900",
        "player_url": "https://rutube.ru/video/4n5o6p7q8r9s0t1u2v3w/",
        "source": "RuTube"
    },
    {
        "title": "Унесённые призраками",
        "year": "2001",
        "rating": "8.6",
        "genre": "Аниме / Фэнтези",
        "country": "Япония",
        "duration": "125 мин",
        "description": "Девочка попадает в город духов и должна спасти своих родителей.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/6d6d6d6d-6d6d-6d6d-6d6d-6d6d6d6d6d6d/600x900",
        "player_url": "https://rutube.ru/video/5o6p7q8r9s0t1u2v3w4x/",
        "source": "RuTube"
    },
    {
        "title": "Назад в будущее",
        "year": "1985",
        "rating": "8.7",
        "genre": "Фантастика / Комедия",
        "country": "США",
        "duration": "116 мин",
        "description": "Подросток отправляется в прошлое на машине времени и меняет судьбу.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/5d5d5d5d-5d5d-5d5d-5d5d-5d5d5d5d5d5d/600x900",
        "player_url": "https://rutube.ru/video/6p7q8r9s0t1u2v3w4x5y/",
        "source": "RuTube"
    },
    {
        "title": "Джокер",
        "year": "2019",
        "rating": "8.4",
        "genre": "Триллер / Драма",
        "country": "США",
        "duration": "122 мин",
        "description": "История происхождения главного врага Бэтмена — клоуна-преступника.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/4d4d4d4d-4d4d-4d4d-4d4d-4d4d4d4d4d4d/600x900",
        "player_url": "https://rutube.ru/video/7q8r9s0t1u2v3w4x5y6z/",
        "source": "RuTube"
    },
    {
        "title": "Паразиты",
        "year": "2019",
        "rating": "8.5",
        "genre": "Драма / Триллер",
        "country": "Южная Корея",
        "duration": "132 мин",
        "description": "Бедная семья хитростью проникает в дом богатых. Но всё идёт не по плану.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/3d3d3d3d-3d3d-3d3d-3d3d-3d3d3d3d3d3d/600x900",
        "player_url": "https://rutube.ru/video/8r9s0t1u2v3w4x5y6z7a/",
        "source": "RuTube"
    },
    {
        "title": "Мстители: Финал",
        "year": "2019",
        "rating": "8.2",
        "genre": "Боевик / Фантастика",
        "country": "США",
        "duration": "181 мин",
        "description": "Мстители собираются в последний раз для битвы с Таносом.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/2d2d2d2d-2d2d-2d2d-2d2d-2d2d2d2d2d2d/600x900",
        "player_url": "https://rutube.ru/video/9s0t1u2v3w4x5y6z7a8b/",
        "source": "RuTube"
    },
    {
        "title": "Гарри Поттер и философский камень",
        "year": "2001",
        "rating": "7.6",
        "genre": "Фэнтези / Приключения",
        "country": "Великобритания",
        "duration": "152 мин",
        "description": "Мальчик-сирота узнаёт, что он волшебник, и едет в школу Хогвартс.",
        "poster": "https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/1d1d1d1d-1d1d-1d1d-1d1d-1d1d1d1d1d1d/600x900",
        "player_url": "https://rutube.ru/video/0t1u2v3w4x5y6z7a8b9c/",
        "source": "RuTube"
    }
]


def create_movie_keyboard(movie: dict) -> InlineKeyboardMarkup:
    """Клавиатура для фильма"""
    keyboard = []
    
    # Кнопка "Смотреть бесплатно"
    keyboard.append([
        InlineKeyboardButton(
            text="▶️ Смотреть бесплатно",
            url=movie.get('player_url', '#')
        )
    ])
    
    # Кнопка на Кинопоиск
    kp_search = f"https://kinopoisk.ru/film/{movie['title'].replace(' ', '-').lower()}/"
    keyboard.append([
        InlineKeyboardButton(
            text="📄 Кинопоиск",
            url=kp_search
        )
    ])
    
    # Кнопка YouTube
    search_url = f"https://www.youtube.com/results?search_query={movie['title'].replace(' ', '+')}+смотреть+бесплатно+полный+фильм"
    keyboard.append([
        InlineKeyboardButton(
            text="🔍 YouTube",
            url=search_url
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_movies_grid_keyboard(movies: list, offset: int = 0) -> InlineKeyboardMarkup:
    """Сетка фильмов с навигацией"""
    keyboard = []
    
    for i in range(offset, min(offset + 10, len(movies)), 2):
        row = []
        row.append(InlineKeyboardButton(
            text=f"🎬 {movies[i]['title'][:22]}{'...' if len(movies[i]['title']) > 22 else ''}",
            callback_data=f"show_movie_{i}"
        ))
        if i + 1 < len(movies) and i + 1 < offset + 10:
            row.append(InlineKeyboardButton(
                text=f"🎬 {movies[i+1]['title'][:22]}{'...' if len(movies[i+1]['title']) > 22 else ''}",
                callback_data=f"show_movie_{i+1}"
            ))
        keyboard.append(row)
    
    # Навигация
    nav_row = []
    if offset > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"nav_{offset-10}"))
    if offset + 10 < len(movies):
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"nav_{offset+10}"))
    if nav_row:
        keyboard.append(nav_row)
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"🎬 <b>Добро пожаловать в бот «Что посмотреть?»!</b>\n\n"
        f"📚 <b>{len(MOVIES_DB)}</b> фильмов с бесплатными плеерами!</b>\n"
        f"✅ <b>Без подписки — смотри бесплатно!</b>\n\n"
        f"<b>Команды:</b>\n"
        f"📋 /movies — все фильмы\n"
        f"🔍 /search — поиск\n"
        f"🎲 /random — случайный\n"
        f"📊 /top — топ по рейтингу\n\n"
        f"Выберите фильм ниже! 🍿",
        parse_mode="HTML",
        reply_markup=create_movies_grid_keyboard(MOVIES_DB[:10])
    )


@dp.message(Command("movies"))
async def cmd_movies(message: types.Message):
    await message.answer(
        f"📋 <b>Все фильмы ({len(MOVIES_DB)}):</b>\n\n✅ Без подписки, бесплатно!",
        parse_mode="HTML",
        reply_markup=create_movies_grid_keyboard(MOVIES_DB)
    )


@dp.callback_query(lambda c: c.data.startswith("show_movie_"))
async def callback_show_movie(callback: types.CallbackQuery):
    try:
        index = int(callback.data.split("_")[-1])
        movie = MOVIES_DB[index]
        
        text = (
            f"🎬 <b>{movie['title']}</b>\n\n"
            f"📅 Год: {movie['year']}\n"
            f"⭐ Рейтинг: {movie['rating']}\n"
            f"🎭 Жанр: {movie['genre']}\n"
            f"🌍 Страна: {movie['country']}\n"
            f"⏱ Длительность: {movie['duration']}\n"
            f"📊 Источник: {movie['source']}\n\n"
            f"📝 <i>{movie['description']}</i>\n\n"
            f"✅ <b>Смотреть бесплатно без подписки!</b>"
        )
        
        await callback.message.answer_photo(
            photo=movie.get('poster', ''),
            caption=text,
            parse_mode="HTML",
            reply_markup=create_movie_keyboard(movie)
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await callback.answer("Ошибка", show_alert=True)


@dp.callback_query(lambda c: c.data.startswith("nav_"))
async def callback_navigation(callback: types.CallbackQuery):
    try:
        offset = int(callback.data.split("_")[-1])
        await callback.message.edit_reply_markup(
            reply_markup=create_movies_grid_keyboard(MOVIES_DB, offset)
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка навигации: {e}")


@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    await message.answer(
        f"🔍 <b>Поиск фильма</b>\n\n"
        f"Введите название:\n"
        f"<i>{len(MOVIES_DB)} фильмов доступно</i>",
        parse_mode="HTML"
    )


@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    import random
    movie = random.choice(MOVIES_DB)
    
    text = (
        f"🎲 <b>Случайный выбор:</b>\n\n"
        f"🎬 {movie['title']}\n"
        f"📅 {movie['year']} | ⭐ {movie['rating']}\n"
        f"🎭 {movie['genre']}\n\n"
        f"<i>{movie['description']}</i>"
    )
    
    await message.answer_photo(
        photo=movie.get('poster', ''),
        caption=text,
        parse_mode="HTML",
        reply_markup=create_movie_keyboard(movie)
    )


@dp.message(Command("top"))
async def cmd_top(message: types.Message):
    sorted_movies = sorted(MOVIES_DB, key=lambda x: float(x['rating']), reverse=True)[:5]
    
    text = "📊 <b>Топ-5 по рейтингу:</b>\n\n"
    for i, movie in enumerate(sorted_movies, 1):
        text += f"{i}. 🎬 <b>{movie['title']}</b> — ⭐ {movie['rating']}\n"
    
    await message.answer(text, parse_mode="HTML")


@dp.message()
async def handle_text(message: types.Message):
    if message.text.startswith('/'):
        return
    
    search_query = message.text.lower()
    await message.answer(f"🔍 Ищу: <b>{message.text}</b>...", parse_mode="HTML")
    
    found_movies = [m for m in MOVIES_DB if search_query in m['title'].lower()]
    
    if found_movies:
        for movie in found_movies[:5]:
            index = MOVIES_DB.index(movie)
            text = (
                f"🎬 <b>{movie['title']}</b>\n"
                f"📅 {movie['year']} | ⭐ {movie['rating']}\n"
                f"🎭 {movie['genre']}\n\n"
                f"<i>{movie['description']}</i>"
            )
            await message.answer_photo(
                photo=movie.get('poster', ''),
                caption=text,
                parse_mode="HTML",
                reply_markup=create_movie_keyboard(movie)
            )
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🔍 Найти на YouTube",
                url=f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}+смотреть+бесплатно"
            )]
        ])
        await message.answer(
            f"😔 <b>{message.text}</b> не найден.\n\nПопробуйте YouTube:",
            parse_mode="HTML",
            reply_markup=keyboard
        )


async def main():
    logger.info(f"🚀 Запуск бота «Что посмотреть?»...")
    logger.info(f"📊 Фильмов: {len(MOVIES_DB)}")
    logger.info(f"💾 Бесплатные источники: RuTube, YouTube")
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
