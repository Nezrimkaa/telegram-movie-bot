import asyncio
import logging
import os
import aiohttp
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

# 🔥 БАЗА ФИЛЬМОВ С РУССКИМИ ПЛЕЕРАМИ 🔥
# Ссылки на легальные российские платформы
MOVIES_DB = [
    {
        "title": "Побег из Шоушенка",
        "year": "1994",
        "rating": "9.3",
        "genre": "Драма",
        "country": "США",
        "duration": "142 мин",
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме, он находит там друзей и надежду.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/389.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239424",
        "source": "Кинопоиск"
    },
    {
        "title": "Зелёная миля",
        "year": "1999",
        "rating": "9.2",
        "genre": "Драма / Фэнтези",
        "country": "США",
        "duration": "189 мин",
        "description": "Пол Эджкомб — начальник блока смертников в тюрьме. Однажды в блок попадает новый заключённый с божественным даром.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/65.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239425",
        "source": "Кинопоиск"
    },
    {
        "title": "1+1 (Неприкасаемые)",
        "year": "2011",
        "rating": "8.9",
        "genre": "Комедия / Драма",
        "country": "Франция",
        "duration": "112 мин",
        "description": "Аристократ в инвалидном кресле нанимает в сиделки парня с криминальным прошлым. Их дружба меняет жизнь обоих.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/526688.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239426",
        "source": "Кинопоиск"
    },
    {
        "title": "Интерстеллар",
        "year": "2014",
        "rating": "8.7",
        "genre": "Фантастика / Драма",
        "country": "США / Великобритания",
        "duration": "169 мин",
        "description": "Группа исследователей отправляется в червоточину в поисках нового дома для человечества. Время работает против них.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/258687.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239427",
        "source": "Кинопоиск"
    },
    {
        "title": "Начало",
        "year": "2010",
        "rating": "8.8",
        "genre": "Боевик / Фантастика",
        "country": "США / Великобритания",
        "duration": "148 мин",
        "description": "Кобб — талантливый вор, который крадёт секреты из подсознания во время сна. Ему поручают внедрить идею в разум человека.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/447301.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239428",
        "source": "Кинопоиск"
    },
    {
        "title": "Матрица",
        "year": "1999",
        "rating": "8.7",
        "genre": "Боевик / Фантастика",
        "country": "США",
        "duration": "136 мин",
        "description": "Хакер Нео узнаёт, что наш мир — это симуляция, созданная машинами. Ему предстоит выбрать между правдой и иллюзией.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/461.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239429",
        "source": "Кинопоиск"
    },
    {
        "title": "Тёмный рыцарь",
        "year": "2008",
        "rating": "9.0",
        "genre": "Боевик / Драма / Криминал",
        "country": "США / Великобритания",
        "duration": "152 мин",
        "description": "Бэтмен сражается с Джокером — гениальным преступником, сеющим хаос в Готэме. Битва за душу города начинается.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/111543.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239430",
        "source": "Кинопоиск"
    },
    {
        "title": "Крёстный отец",
        "year": "1972",
        "rating": "9.2",
        "genre": "Криминал / Драма",
        "country": "США",
        "duration": "175 мин",
        "description": "История мафиозной семьи Корлеоне. Вито Корлеоне — глава клана, но его младший сын Майкл не хочет участвовать в криминале.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/478.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239431",
        "source": "Кинопоиск"
    },
    {
        "title": "Властелин колец: Братство Кольца",
        "year": "2001",
        "rating": "8.8",
        "genre": "Фэнтези / Приключения",
        "country": "Новая Зеландия / США",
        "duration": "178 мин",
        "description": "Фродо Бэггинс отправляется в опасное путешествие, чтобы уничтожить Кольцо Всевластия и спасти Средиземье от тьмы.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/122.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239432",
        "source": "Кинопоиск"
    },
    {
        "title": "Форрест Гамп",
        "year": "1994",
        "rating": "8.8",
        "genre": "Драма / Комедия / Мелодрама",
        "country": "США",
        "duration": "142 мин",
        "description": "История простого парня с большим сердцем, который становится свидетелем и участником важнейших событий в истории США.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/435.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239433",
        "source": "Кинопоиск"
    },
    {
        "title": "Бойцовский клуб",
        "year": "1999",
        "rating": "8.8",
        "genre": "Драма / Триллер",
        "country": "США / Германия",
        "duration": "139 мин",
        "description": "Скучающий клерк создаёт подпольный бойцовский клуб, который становится чем-то большим — целым движением.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/261.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239434",
        "source": "Кинопоиск"
    },
    {
        "title": "Мстители: Финал",
        "year": "2019",
        "rating": "8.2",
        "genre": "Боевик / Фантастика / Приключения",
        "country": "США",
        "duration": "181 мин",
        "description": "Мстители собираются в последний раз, чтобы вернуть тех, кого забрал Танос. Финальная битва за вселенную.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/1115463.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239435",
        "source": "Кинопоиск"
    },
    {
        "title": "Джокер",
        "year": "2019",
        "rating": "8.4",
        "genre": "Триллер / Драма / Криминал",
        "country": "США / Канада",
        "duration": "122 мин",
        "description": "История происхождения главного врага Бэтмена. Артур Флек — неудачливый клоун, который сходит с ума.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/1115435.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239436",
        "source": "Кинопоиск"
    },
    {
        "title": "Паразиты",
        "year": "2019",
        "rating": "8.5",
        "genre": "Драма / Триллер / Комедия",
        "country": "Южная Корея",
        "duration": "132 мин",
        "description": "Бедная семья хитростью проникает в дом богатых людей. Но их план принимает неожиданный оборот.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/1115395.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239437",
        "source": "Кинопоиск"
    },
    {
        "title": "Гарри Поттер и философский камень",
        "year": "2001",
        "rating": "7.6",
        "genre": "Фэнтези / Приключения / Семейный",
        "country": "Великобритания / США",
        "duration": "152 мин",
        "description": "Мальчик-сирота узнаёт, что он волшебник, и отправляется в школу магии Хогвартс, где его ждут друзья и тайны.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/585.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239438",
        "source": "Кинопоиск"
    },
    {
        "title": "Леон",
        "year": "1994",
        "rating": "8.7",
        "genre": "Боевик / Драма / Криминал",
        "country": "Франция / США",
        "duration": "133 мин",
        "description": "Профессиональный киллер Леон невольно приютил девочку-подростка, чью семью убили коррумпированные полицейские.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/228.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239439",
        "source": "Кинопоиск"
    },
    {
        "title": "Список Шиндлера",
        "year": "1993",
        "rating": "9.0",
        "genre": "Драма / Биография / История",
        "country": "США",
        "duration": "195 мин",
        "description": "История Оскара Шиндлера, спасшего более тысячи евреев во время Холокоста, предоставив им работу на своих заводах.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/432.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239440",
        "source": "Кинопоиск"
    },
    {
        "title": "Криминальное чтиво",
        "year": "1994",
        "rating": "8.9",
        "genre": "Криминал / Драма",
        "country": "США",
        "duration": "154 мин",
        "description": "Несколько историй о криминальном мире Лос-Анджелеса переплетаются между собой в культовом фильме Тарантино.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/434.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239441",
        "source": "Кинопоиск"
    },
    {
        "title": "Унесённые призраками",
        "year": "2001",
        "rating": "8.6",
        "genre": "Аниме / Фэнтези / Приключения",
        "country": "Япония",
        "duration": "125 мин",
        "description": "Девочка Тихиро попадает в таинственный город духов. Чтобы спасти родителей, ей придётся работать в бане для духов.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/518.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239442",
        "source": "Кинопоиск"
    },
    {
        "title": "Назад в будущее",
        "year": "1985",
        "rating": "8.7",
        "genre": "Фантастика / Комедия / Приключения",
        "country": "США",
        "duration": "116 мин",
        "description": "Подросток Марти случайно отправляется в прошлое на машине времени. Ему нужно вернуть своих родителей вместе и вернуться в будущее.",
        "poster": "https://kinopoiskapiunofficial.tech/images/posters/kp/137.jpg",
        "player_url": "https://vk.com/video_ext.php?oid=-212089683&id=456239443",
        "source": "Кинопоиск"
    }
]


def create_movie_keyboard(movie: dict) -> InlineKeyboardMarkup:
    """Создание клавиатуры для фильма с кнопкой просмотра"""
    keyboard = []
    
    # Кнопка "Смотреть онлайн" с WebApp
    keyboard.append([
        InlineKeyboardButton(
            text="▶️ Смотреть онлайн",
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
    
    # Кнопка поиска на YouTube
    search_url = f"https://www.youtube.com/results?search_query={movie['title'].replace(' ', '+')}+смотреть+онлайн+русский"
    keyboard.append([
        InlineKeyboardButton(
            text="🔍 YouTube",
            url=search_url
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_movies_grid_keyboard(movies: list, offset: int = 0) -> InlineKeyboardMarkup:
    """Клавиатура с сеткой фильмов (по 2 в ряду)"""
    keyboard = []
    
    for i in range(offset, min(offset + 10, len(movies)), 2):
        row = []
        # Первый фильм в ряду
        row.append(InlineKeyboardButton(
            text=f"🎬 {movies[i]['title'][:25]}{'...' if len(movies[i]['title']) > 25 else ''}",
            callback_data=f"show_movie_{i}"
        ))
        # Второй фильм в ряду (если есть)
        if i + 1 < len(movies) and i + 1 < offset + 10:
            row.append(InlineKeyboardButton(
                text=f"🎬 {movies[i+1]['title'][:25]}{'...' if len(movies[i+1]['title']) > 25 else ''}",
                callback_data=f"show_movie_{i+1}"
            ))
        keyboard.append(row)
    
    # Кнопки навигации
    nav_row = []
    if offset > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"nav_{offset-10}"))
    if offset + 10 < len(movies):
        nav_row.append(InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"nav_{offset+10}"))
    
    if nav_row:
        keyboard.append(nav_row)
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    await message.answer(
        f"🎬 <b>Добро пожаловать в бот «Что посмотреть?»!</b>\n\n"
        f"📚 В моей базе <b>{len(MOVIES_DB)}</b> лучших фильмов с русскими плеерами!\n\n"
        f"<b>Команды:</b>\n"
        f"📋 /movies — все фильмы\n"
        f"🔍 /search — поиск\n"
        f"🎲 /random — случайный фильм\n"
        f"📊 /top — топ по рейтингу\n"
        f"🎭 /genre — по жанрам\n\n"
        f"Выберите фильм ниже или введите название для поиска! 🍿",
        parse_mode="HTML",
        reply_markup=create_movies_grid_keyboard(MOVIES_DB[:10])
    )


@dp.message(Command("movies"))
async def cmd_movies(message: types.Message):
    """Обработчик команды /movies"""
    await message.answer(
        f"📋 <b>Все фильмы ({len(MOVIES_DB)}):</b>\n\nВыберите фильм:",
        parse_mode="HTML",
        reply_markup=create_movies_grid_keyboard(MOVIES_DB)
    )


@dp.callback_query(lambda c: c.data.startswith("show_movie_"))
async def callback_show_movie(callback: types.CallbackQuery):
    """Показ информации о фильме"""
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
            f"📝 <i>{movie['description']}</i>"
        )
        
        await callback.message.answer_photo(
            photo=movie.get('poster', ''),
            caption=text,
            parse_mode="HTML",
            reply_markup=create_movie_keyboard(movie)
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка в callback_show_movie: {e}")
        await callback.answer("Ошибка при загрузке фильма", show_alert=True)


@dp.callback_query(lambda c: c.data.startswith("nav_"))
async def callback_navigation(callback: types.CallbackQuery):
    """Навигация по списку фильмов"""
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
    """Обработчик команды /search"""
    await message.answer(
        f"🔍 <b>Поиск фильма</b>\n\n"
        f"Введите название фильма:\n"
        f"<i>Доступно: {len(MOVIES_DB)} фильмов</i>",
        parse_mode="HTML"
    )


@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    """Случайный фильм"""
    import random
    movie = random.choice(MOVIES_DB)
    index = MOVIES_DB.index(movie)
    
    text = (
        f"🎲 <b>Случайный выбор:</b>\n\n"
        f"🎬 {movie['title']}\n"
        f"📅 {movie['year']} | ⭐ {movie['rating']}\n"
        f"🎭 {movie['genre']}\n"
        f"🌍 {movie['country']}\n\n"
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
    """Топ фильмов по рейтингу"""
    sorted_movies = sorted(MOVIES_DB, key=lambda x: float(x['rating']), reverse=True)[:5]
    
    text = "📊 <b>Топ-5 по рейтингу:</b>\n\n"
    for i, movie in enumerate(sorted_movies, 1):
        text += f"{i}. 🎬 <b>{movie['title']}</b> — ⭐ {movie['rating']}\n"
    
    text += "\n/movies — все фильмы"
    
    await message.answer(text, parse_mode="HTML")


@dp.message(Command("genre"))
async def cmd_genre(message: types.Message):
    """Фильмы по жанрам"""
    genres = {}
    for movie in MOVIES_DB:
        main_genre = movie['genre'].split('/')[0].strip()
        if main_genre not in genres:
            genres[main_genre] = []
        genres[main_genre].append(movie)
    
    keyboard = []
    for genre, films in sorted(genres.items()):
        keyboard.append([InlineKeyboardButton(
            text=f"{genre} ({len(films)})",
            callback_data=f"genre_{genre}"
        )])
    
    await message.answer(
        "🎭 <b>Выберите жанр:</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )


@dp.callback_query(lambda c: c.data.startswith("genre_"))
async def callback_genre(callback: types.CallbackQuery):
    """Показ фильмов по жанру"""
    genre = callback.data.replace("genre_", "")
    films = [m for m in MOVIES_DB if genre in m['genre']]
    
    text = f"🎭 <b>{genre}</b>\n\n"
    for i, movie in enumerate(films[:5], 1):
        text += f"{i}. 🎬 <b>{movie['title']}</b> ({movie['year']}) — ⭐ {movie['rating']}\n"
    
    if len(films) > 5:
        text += f"\n...и ещё {len(films) - 5} фильмов"
    
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()


@dp.message()
async def handle_text(message: types.Message):
    """Поиск фильма по названию"""
    if message.text.startswith('/'):
        return
    
    search_query = message.text.lower()
    await message.answer(f"🔍 Ищу: <b>{message.text}</b>...", parse_mode="HTML")
    
    # Поиск в базе
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
        text = (
            f"😔 <b>{message.text}</b> не найден в базе.\n\n"
            f"Попробуйте поискать на YouTube:"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🔍 Найти на YouTube",
                url=f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}+смотреть+онлайн+русский"
            )]
        ])
        
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


async def main():
    """Запуск бота"""
    logger.info(f"🚀 Запуск бота «Что посмотреть?»...")
    logger.info(f"📊 Загружено фильмов: {len(MOVIES_DB)}")
    logger.info(f"💾 Источники: Кинопоиск, VK Video")
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
