import asyncio
import logging
import re
from typing import Optional

import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from bs4 import BeautifulSoup

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Замените на ваш токен от @BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# База данных фильмов (будет заполнена при парсинге)
movies_db = []


class MovieParser:
    """Парсер фильмов с популярных сайтов"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }
    
    async def start_session(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
    
    async def close_session(self):
        if self.session:
            await self.session.close()
    
    async def parse_kinopoisk(self, limit: int = 10) -> list:
        """Парсинг популярных фильмов с Кинопоиска"""
        movies = []
        try:
            url = "https://www.kinopoisk.ru/top/250/"
            async with self.session.get(url, timeout=15) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    film_cards = soup.select('.top250__listitem')[:limit]
                    
                    for card in film_cards:
                        try:
                            title_elem = card.select_one('.top250__title')
                            rating_elem = card.select_one('.top250__rating')
                            year_elem = card.select_one('.top250__year')
                            link_elem = card.select_one('a[href*="/film/"]')
                            
                            if title_elem and link_elem:
                                title = title_elem.get_text(strip=True)
                                rating = rating_elem.get_text(strip=True) if rating_elem else "N/A"
                                year = year_elem.get_text(strip=True) if year_elem else "N/A"
                                link = "https://www.kinopoisk.ru" + link_elem.get('href') if link_elem.get('href') else ""
                                
                                movies.append({
                                    'title': title,
                                    'year': year,
                                    'rating': rating,
                                    'source': 'Кинопоиск',
                                    'link': link,
                                    'poster': None,
                                    'player_url': self._get_player_url(title)
                                })
                        except Exception as e:
                            logger.warning(f"Ошибка парсинга фильма: {e}")
                            
        except Exception as e:
            logger.error(f"Ошибка парсинга Кинопоиска: {e}")
        
        return movies
    
    async def parse_imdb_top(self, limit: int = 10) -> list:
        """Парсинг топ фильмов с IMDb"""
        movies = []
        try:
            url = "https://www.imdb.com/chart/top/"
            async with self.session.get(url, timeout=15) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    film_cards = soup.select('li.ipc-metadata-list__item')[:limit]
                    
                    for card in film_cards:
                        try:
                            title_elem = card.select_one('h3.ipc-title__text a')
                            rating_elem = card.select_one('span.ipc-rating-value')
                            year_elem = card.select_one('span.sc-b189961a-8')
                            
                            if title_elem:
                                title = title_elem.get_text(strip=True)
                                rating = rating_elem.get_text(strip=True) if rating_elem else "N/A"
                                year = year_elem.get_text(strip=True) if year_elem else "N/A"
                                link = "https://www.imdb.com" + title_elem.get('href') if title_elem.get('href') else ""
                                
                                movies.append({
                                    'title': title,
                                    'year': year,
                                    'rating': rating,
                                    'source': 'IMDb',
                                    'link': link,
                                    'poster': None,
                                    'player_url': self._get_player_url(title)
                                })
                        except Exception as e:
                            logger.warning(f"Ошибка парсинга IMDb фильма: {e}")
                            
        except Exception as e:
            logger.error(f"Ошибка парсинга IMDb: {e}")
        
        return movies
    
    def _get_player_url(self, title: str) -> str:
        """Генерация ссылки на встроенный плеер YouTube с фильмом"""
        search_query = title.replace(' ', '+').replace(':', '')
        return f"https://www.youtube.com/embed?listType=search&list={search_query}+full+movie+with+subtitles"
    
    async def search_movie_on_youtube(self, title: str) -> str:
        """Поиск фильма на YouTube для просмотра"""
        search_query = f"{title} смотреть онлайн".replace(' ', '+')
        return f"https://www.youtube.com/results?search_query={search_query}"


async def parse_movies() -> list:
    """Основная функция парсинга фильмов"""
    parser = MovieParser()
    await parser.start_session()
    
    try:
        kinopoisk_movies = await parser.parse_kinopoisk(limit=5)
        imdb_movies = await parser.parse_imdb_top(limit=5)
        
        all_movies = kinopoisk_movies + imdb_movies
        logger.info(f"Спарсено {len(all_movies)} фильмов")
        
        return all_movies
    finally:
        await parser.close_session()


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
    
    # Кнопка с ссылкой на источник
    if movie.get('link'):
        keyboard.append([
            InlineKeyboardButton(
                text=f"📄 Информация ({movie.get('source', '')})",
                url=movie['link']
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
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    await message.answer(
        "🎬 <b>Добро пожаловать в бот «Что посмотреть?»!</b>\n\n"
        "Я помогу вам выбрать фильм для просмотра. "
        "Нажмите /movies чтобы увидеть подборку лучших фильмов "
        "или /search чтобы найти конкретный фильм.\n\n"
        "Все фильмы доступны для просмотра через встроенный плеер! 🍿",
        parse_mode="HTML"
    )


@dp.message(Command("movies"))
async def cmd_movies(message: types.Message):
    """Обработчик команды /movies - показывает список фильмов"""
    global movies_db
    
    if not movies_db:
        wait_msg = await message.answer("⏳ Загружаю подборку фильмов...")
        movies_db = await parse_movies()
        await wait_msg.delete()
    
    if not movies_db:
        await message.answer("😔 Не удалось загрузить фильмы. Попробуйте позже.")
        return
    
    for i, movie in enumerate(movies_db[:5]):
        text = (
            f"🎬 <b>{movie['title']}</b>\n"
            f"📅 Год: {movie.get('year', 'N/A')}\n"
            f"⭐ Рейтинг: {movie.get('rating', 'N/A')}\n"
            f"📊 Источник: {movie.get('source', 'N/A')}"
        )
        
        await message.answer(
            text,
            parse_mode="HTML",
            reply_markup=create_movie_keyboard(movie)
        )
        
        if i < 4:
            await asyncio.sleep(0.3)


@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    """Обработчик команды /search - поиск фильма"""
    await message.answer(
        "🔍 Введите название фильма для поиска:\n\n"
        "Я найду информацию о фильме и ссылку для просмотра."
    )


@dp.message()
async def handle_text(message: types.Message):
    """Обработчик текстовых сообщений - поиск фильма"""
    if message.text.startswith('/'):
        return
    
    search_query = message.text
    await message.answer(f"🔍 Ищу фильм: <b>{search_query}</b>...", parse_mode="HTML")
    
    found_movies = [m for m in movies_db if search_query.lower() in m['title'].lower()]
    
    if found_movies:
        for movie in found_movies[:3]:
            text = (
                f"🎬 <b>{movie['title']}</b>\n"
                f"📅 Год: {movie.get('year', 'N/A')}\n"
                f"⭐ Рейтинг: {movie.get('rating', 'N/A')}"
            )
            await message.answer(
                text,
                parse_mode="HTML",
                reply_markup=create_movie_keyboard(movie)
            )
    else:
        movie = {
            'title': search_query,
            'year': 'N/A',
            'rating': 'N/A',
            'source': 'Поиск',
            'link': '',
            'player_url': f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}+смотреть+онлайн"
        }
        
        text = f"🎬 <b>{search_query}</b>\n\nФильм не найден в базе, но вы можете посмотреть его на YouTube:"
        await message.answer(
            text,
            parse_mode="HTML",
            reply_markup=create_movie_keyboard(movie)
        )


async def main():
    """Запуск бота"""
    logger.info("Запуск бота...")
    
    global movies_db
    movies_db = await parse_movies()
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
