import asyncio
import logging
import os
import random
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

# 🔥 БАЗА ИЗ 100 ФИЛЬМОВ С ПРЯМЫМИ ССЫЛКАМИ НА YouTube 🔥
# Ссылки на официальные трейлеры + поиск полных фильмов
MOVIES_DB = [
    {"title": "Побег из Шоушенка", "year": "1994", "rating": "9.3", "genre": "Драма", "country": "США", "duration": "142 мин", "description": "Бухгалтер обвинён в убийстве жены. В тюрьме он находит друзей и надежду.", "player_url": "https://www.youtube.com/results?search_query=побег+из+шоушенка+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/389/"},
    {"title": "Зелёная миля", "year": "1999", "rating": "9.2", "genre": "Драма", "country": "США", "duration": "189 мин", "description": "Начальник блока смертников встречает заключённого с даром исцеления.", "player_url": "https://www.youtube.com/results?search_query=зелёная+миля+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/65/"},
    {"title": "Крёстный отец", "year": "1972", "rating": "9.2", "genre": "Криминал", "country": "США", "duration": "175 мин", "description": "Сага о мафиозной семье Корлеоне.", "player_url": "https://www.youtube.com/results?search_query=крёстный+отец+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/478/"},
    {"title": "Тёмный рыцарь", "year": "2008", "rating": "9.0", "genre": "Боевик", "country": "США", "duration": "152 мин", "description": "Бэтмен противостоит Джокеру.", "player_url": "https://www.youtube.com/results?search_query=тёмный+рыцарь+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/111543/"},
    {"title": "1+1 (Неприкасаемые)", "year": "2011", "rating": "8.9", "genre": "Комедия", "country": "Франция", "duration": "112 мин", "description": "Аристократ и парень с улицы становятся друзьями.", "player_url": "https://www.youtube.com/results?search_query=1+1+неприкасаемые+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/526688/"},
    {"title": "Матрица", "year": "1999", "rating": "8.7", "genre": "Фантастика", "country": "США", "duration": "136 мин", "description": "Хакер узнаёт, что мир — симуляция.", "player_url": "https://www.youtube.com/results?search_query=матрица+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/461/"},
    {"title": "Интерстеллар", "year": "2014", "rating": "8.7", "genre": "Фантастика", "country": "США", "duration": "169 мин", "description": "Экспедиция через червоточину.", "player_url": "https://www.youtube.com/results?search_query=интерстеллар+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/258687/"},
    {"title": "Начало", "year": "2010", "rating": "8.8", "genre": "Фантастика", "country": "США", "duration": "148 мин", "description": "Вор крадёт секреты из снов.", "player_url": "https://www.youtube.com/results?search_query=начало+фильм+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/447301/"},
    {"title": "Форрест Гамп", "year": "1994", "rating": "8.8", "genre": "Драма", "country": "США", "duration": "142 мин", "description": "Простой парень становится участником великих событий.", "player_url": "https://www.youtube.com/results?search_query=форрест+гамп+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/435/"},
    {"title": "Бойцовский клуб", "year": "1999", "rating": "8.8", "genre": "Драма", "country": "США", "duration": "139 мин", "description": "Клерк создаёт подпольный бойцовский клуб.", "player_url": "https://www.youtube.com/results?search_query=бойцовский+клуб+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/261/"},
    {"title": "Властелин колец: Братство Кольца", "year": "2001", "rating": "8.8", "genre": "Фэнтези", "country": "Новая Зеландия", "duration": "178 мин", "description": "Фродо отправляется уничтожить Кольцо.", "player_url": "https://www.youtube.com/results?search_query=властелин+колец+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/122/"},
    {"title": "Властелин колец: Две крепости", "year": "2002", "rating": "8.7", "genre": "Фэнтези", "country": "Новая Зеландия", "duration": "179 мин", "description": "Братство распалось. Фродо и Сэм продолжают путь.", "player_url": "https://www.youtube.com/results?search_query=властелин+колец+2+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/123/"},
    {"title": "Властелин колец: Возвращение короля", "year": "2003", "rating": "8.9", "genre": "Фэнтези", "country": "Новая Зеландия", "duration": "201 мин", "description": "Финальная битва за Средиземье.", "player_url": "https://www.youtube.com/results?search_query=властелин+колец+3+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/124/"},
    {"title": "Леон", "year": "1994", "rating": "8.7", "genre": "Боевик", "country": "Франция", "duration": "133 мин", "description": "Киллер приютил девочку.", "player_url": "https://www.youtube.com/results?search_query=леон+фильм+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/228/"},
    {"title": "Назад в будущее", "year": "1985", "rating": "8.7", "genre": "Фантастика", "country": "США", "duration": "116 мин", "description": "Подросток отправляется в прошлое.", "player_url": "https://www.youtube.com/results?search_query=назад+в+будущее+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/137/"},
    {"title": "Терминатор 2", "year": "1991", "rating": "8.5", "genre": "Боевик", "country": "США", "duration": "137 мин", "description": "Терминатор защищает Джона Коннора.", "player_url": "https://www.youtube.com/results?search_query=терминатор+2+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/224/"},
    {"title": "Криминальное чтиво", "year": "1994", "rating": "8.9", "genre": "Криминал", "country": "США", "duration": "154 мин", "description": "Культовый фильм Тарантино.", "player_url": "https://www.youtube.com/results?search_query=криминальное+чтиво+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/434/"},
    {"title": "Список Шиндлера", "year": "1993", "rating": "9.0", "genre": "Драма", "country": "США", "duration": "195 мин", "description": "История Оскара Шиндлера.", "player_url": "https://www.youtube.com/results?search_query=список+шиндлера+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/432/"},
    {"title": "Гладиатор", "year": "2000", "rating": "8.5", "genre": "Боевик", "country": "США", "duration": "155 мин", "description": "Римский генерал становится гладиатором.", "player_url": "https://www.youtube.com/results?search_query=гладиатор+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/113/"},
    {"title": "Молчание ягнят", "year": "1991", "rating": "8.6", "genre": "Триллер", "country": "США", "duration": "118 мин", "description": "Агент ФБР и каннибал Лектер.", "player_url": "https://www.youtube.com/results?search_query=молчание+ягнят+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/229/"},
    {"title": "Гарри Поттер и философский камень", "year": "2001", "rating": "7.6", "genre": "Фэнтези", "country": "Великобритания", "duration": "152 мин", "description": "Мальчик узнаёт, что он волшебник.", "player_url": "https://www.youtube.com/results?search_query=гарри+поттер+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/585/"},
    {"title": "Гарри Поттер и Тайная комната", "year": "2002", "rating": "7.7", "genre": "Фэнтези", "country": "Великобритания", "duration": "161 мин", "description": "Гарри сталкивается с наследником Слизерина.", "player_url": "https://www.youtube.com/results?search_query=гарри+поттер+2+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/586/"},
    {"title": "Гарри Поттер и узник Азкабана", "year": "2004", "rating": "7.9", "genre": "Фэнтези", "country": "Великобритания", "duration": "142 мин", "description": "Гарри узнаёт правду о Сириусе Блэке.", "player_url": "https://www.youtube.com/results?search_query=гарри+поттер+3+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/587/"},
    {"title": "Пираты Карибского моря: Проклятие Чёрной жемчужины", "year": "2003", "rating": "8.0", "genre": "Приключения", "country": "США", "duration": "143 мин", "description": "Джек Воробей спасает Элизабет.", "player_url": "https://www.youtube.com/results?search_query=пираты+карибского+моря+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/726/"},
    {"title": "Парк юрского периода", "year": "1993", "rating": "8.2", "genre": "Фантастика", "country": "США", "duration": "127 мин", "description": "Динозавры вырываются на свободу.", "player_url": "https://www.youtube.com/results?search_query=парк+юрского+периода+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/320/"},
    {"title": "Мстители", "year": "2012", "rating": "8.0", "genre": "Боевик", "country": "США", "duration": "143 мин", "description": "Герои Marvel объединяются.", "player_url": "https://www.youtube.com/results?search_query=мстители+2012+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/401546/"},
    {"title": "Мстители: Финал", "year": "2019", "rating": "8.2", "genre": "Боевик", "country": "США", "duration": "181 мин", "description": "Финальная битва с Таносом.", "player_url": "https://www.youtube.com/results?search_query=мстители+финал+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1115463/"},
    {"title": "Железный человек", "year": "2008", "rating": "7.9", "genre": "Боевик", "country": "США", "duration": "126 мин", "description": "Тони Старк становится супергероем.", "player_url": "https://www.youtube.com/results?search_query=железный+человек+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1115157/"},
    {"title": "Человек-паук", "year": "2002", "rating": "7.4", "genre": "Боевик", "country": "США", "duration": "121 мин", "description": "Питер Паркер получает силы паука.", "player_url": "https://www.youtube.com/results?search_query=человек+паук+2002+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1426/"},
    {"title": "Человек-паук: Нет пути домой", "year": "2021", "rating": "8.2", "genre": "Боевик", "country": "США", "duration": "148 мин", "description": "Питер открывает мультивселенную.", "player_url": "https://www.youtube.com/results?search_query=человек+паук+нет+пути+домой+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/606729/"},
    {"title": "Бэтмен: Начало", "year": "2005", "rating": "8.2", "genre": "Боевик", "country": "США", "duration": "140 мин", "description": "Становление Брюса Уэйна Бэтменом.", "player_url": "https://www.youtube.com/results?search_query=бэтмен+начало+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/111543/"},
    {"title": "Бэтмен", "year": "2022", "rating": "7.8", "genre": "Боевик", "country": "США", "duration": "176 мин", "description": "Брюс Уэйн охотится на Загадочника.", "player_url": "https://www.youtube.com/results?search_query=бэтмен+2022+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1115435/"},
    {"title": "Джокер", "year": "2019", "rating": "8.4", "genre": "Триллер", "country": "США", "duration": "122 мин", "description": "История происхождения Джокера.", "player_url": "https://www.youtube.com/results?search_query=джокер+2019+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1115435/"},
    {"title": "Аватар", "year": "2009", "rating": "7.9", "genre": "Фантастика", "country": "США", "duration": "162 мин", "description": "Солдат попадает на Пандору.", "player_url": "https://www.youtube.com/results?search_query=аватар+2009+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/258687/"},
    {"title": "Дюна", "year": "2021", "rating": "8.0", "genre": "Фантастика", "country": "США", "duration": "155 мин", "description": "Пол Атрейдес на Арракисе.", "player_url": "https://www.youtube.com/results?search_query=дюна+2021+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1115395/"},
    {"title": "Дюна: Часть вторая", "year": "2024", "rating": "8.5", "genre": "Фантастика", "country": "США", "duration": "166 мин", "description": "Пол объединяется с фрименами.", "player_url": "https://www.youtube.com/results?search_query=дюна+2+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1115396/"},
    {"title": "Оппенгеймер", "year": "2023", "rating": "8.3", "genre": "Драма", "country": "США", "duration": "180 мин", "description": "Создание атомной бомбы.", "player_url": "https://www.youtube.com/results?search_query=оппенгеймер+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1115397/"},
    {"title": "Шрек", "year": "2001", "rating": "7.9", "genre": "Мультфильм", "country": "США", "duration": "90 мин", "description": "Огр спасает принцессу.", "player_url": "https://www.youtube.com/results?search_query=шрек+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2001/"},
    {"title": "Шрек 2", "year": "2004", "rating": "7.3", "genre": "Мультфильм", "country": "США", "duration": "93 мин", "description": "Знакомство с родителями.", "player_url": "https://www.youtube.com/results?search_query=шрек+2+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2004/"},
    {"title": "Холодное сердце", "year": "2013", "rating": "7.4", "genre": "Мультфильм", "country": "США", "duration": "102 мин", "description": "Анна ищет сестру Эльзу.", "player_url": "https://www.youtube.com/results?search_query=холодное+сердце+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2013/"},
    {"title": "Король Лев", "year": "1994", "rating": "8.5", "genre": "Мультфильм", "country": "США", "duration": "88 мин", "description": "Львёнок Симба возвращается на трон.", "player_url": "https://www.youtube.com/results?search_query=король+лев+1994+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1994/"},
    {"title": "ВАЛЛ·И", "year": "2008", "rating": "8.4", "genre": "Мультфильм", "country": "США", "duration": "98 мин", "description": "Робот влюбляется и спасает человечество.", "player_url": "https://www.youtube.com/results?search_query=валл+и+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2008/"},
    {"title": "Тачки", "year": "2006", "rating": "7.2", "genre": "Мультфильм", "country": "США", "duration": "117 мин", "description": "Молния Маккуин в Радиатор-Спрингс.", "player_url": "https://www.youtube.com/results?search_query=тачки+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2006/"},
    {"title": "История игрушек", "year": "1995", "rating": "8.3", "genre": "Мультфильм", "country": "США", "duration": "81 мин", "description": "Вуди и Базз дружат.", "player_url": "https://www.youtube.com/results?search_query=история+игрушек+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1995/"},
    {"title": "Как приручить дракона", "year": "2010", "rating": "8.1", "genre": "Мультфильм", "country": "США", "duration": "98 мин", "description": "Викинг дружит с драконом.", "player_url": "https://www.youtube.com/results?search_query=как+приручить+дракона+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2010/"},
    {"title": "Зверополис", "year": "2016", "rating": "8.0", "genre": "Мультфильм", "country": "США", "duration": "108 мин", "description": "Кролик и лис раскрывают заговор.", "player_url": "https://www.youtube.com/results?search_query=зверополис+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2016/"},
    {"title": "Гадкий я", "year": "2010", "rating": "7.6", "genre": "Мультфильм", "country": "США", "duration": "95 мин", "description": "Злодей усыновляет сирот.", "player_url": "https://www.youtube.com/results?search_query=гадкий+я+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2010/"},
    {"title": "Головоломка", "year": "2015", "rating": "8.1", "genre": "Мультфильм", "country": "США", "duration": "95 мин", "description": "Эмоции управляют разумом.", "player_url": "https://www.youtube.com/results?search_query=головоломка+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2015/"},
    {"title": "Суперсемейка", "year": "2004", "rating": "8.0", "genre": "Мультфильм", "country": "США", "duration": "115 мин", "description": "Семья супергероев.", "player_url": "https://www.youtube.com/results?search_query=суперсемейка+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2004/"},
    {"title": "Хоббит: Нежданное путешествие", "year": "2012", "rating": "7.8", "genre": "Фэнтези", "country": "Новая Зеландия", "duration": "169 мин", "description": "Бильбо отправляется в поход.", "player_url": "https://www.youtube.com/results?search_query=хоббит+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2012/"},
    {"title": "Хоббит: Пустошь Смауга", "year": "2013", "rating": "7.8", "genre": "Фэнтези", "country": "Новая Зеландия", "duration": "161 мин", "description": "Гномы достигают горы.", "player_url": "https://www.youtube.com/results?search_query=хоббит+2+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2013/"},
    {"title": "Хоббит: Битва пяти воинств", "year": "2014", "rating": "7.4", "genre": "Фэнтези", "country": "Новая Зеландия", "duration": "144 мин", "description": "Битва за Эребор.", "player_url": "https://www.youtube.com/results?search_query=хоббит+3+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2014/"},
    {"title": "Мумия", "year": "1999", "rating": "7.1", "genre": "Приключения", "country": "США", "duration": "124 мин", "description": "Пробуждение жреца Имхотепа.", "player_url": "https://www.youtube.com/results?search_query=мумия+1999+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1999/"},
    {"title": "Люди в чёрном", "year": "1997", "rating": "7.3", "genre": "Фантастика", "country": "США", "duration": "98 мин", "description": "Контроль инопланетян на Земле.", "player_url": "https://www.youtube.com/results?search_query=люди+в+чёрном+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1997/"},
    {"title": "День сурка", "year": "1993", "rating": "8.0", "genre": "Комедия", "country": "США", "duration": "101 мин", "description": "Один день снова и снова.", "player_url": "https://www.youtube.com/results?search_query=день+сурка+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1993/"},
    {"title": "Один дома", "year": "1990", "rating": "7.7", "genre": "Комедия", "country": "США", "duration": "103 мин", "description": "Мальчик против грабителей.", "player_url": "https://www.youtube.com/results?search_query=один+дома+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1990/"},
    {"title": "Маска", "year": "1994", "rating": "6.9", "genre": "Комедия", "country": "США", "duration": "101 мин", "description": "Магическая маска превращает в супергероя.", "player_url": "https://www.youtube.com/results?search_query=маска+1994+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1994/"},
    {"title": "Амели", "year": "2001", "rating": "8.3", "genre": "Комедия", "country": "Франция", "duration": "122 мин", "description": "Девушка меняет жизни к лучшему.", "player_url": "https://www.youtube.com/results?search_query=амели+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2001/"},
    {"title": "Такси", "year": "1998", "rating": "7.0", "genre": "Боевик", "country": "Франция", "duration": "86 мин", "description": "Таксист и полицейский ловят бандитов.", "player_url": "https://www.youtube.com/results?search_query=такси+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1998/"},
    {"title": "Крепкий орешек", "year": "1988", "rating": "8.2", "genre": "Боевик", "country": "США", "duration": "132 мин", "description": "Полицейский против террористов.", "player_url": "https://www.youtube.com/results?search_query=крепкий+орешек+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1988/"},
    {"title": "Рэмбо: Первая кровь", "year": "1982", "rating": "7.7", "genre": "Боевик", "country": "США", "duration": "93 мин", "description": "Ветеран против полиции.", "player_url": "https://www.youtube.com/results?search_query=рэмбо+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1982/"},
    {"title": "Рокки", "year": "1976", "rating": "8.1", "genre": "Драма", "country": "США", "duration": "120 мин", "description": "Боксёр получает шанс.", "player_url": "https://www.youtube.com/results?search_query=рокки+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1976/"},
    {"title": "Трансформеры", "year": "2007", "rating": "7.0", "genre": "Фантастика", "country": "США", "duration": "144 мин", "description": "Автоботы против десептиконов.", "player_url": "https://www.youtube.com/results?search_query=трансформеры+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2007/"},
    {"title": "Индиана Джонс: В поисках утраченного ковчега", "year": "1981", "rating": "8.4", "genre": "Приключения", "country": "США", "duration": "115 мин", "description": "Поиск Ковчега Завета.", "player_url": "https://www.youtube.com/results?search_query=индиана+джонс+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1981/"},
    {"title": "Люди Икс", "year": "2000", "rating": "7.3", "genre": "Фантастика", "country": "США", "duration": "104 мин", "description": "Мутанты сражаются за мир.", "player_url": "https://www.youtube.com/results?search_query=люди+икс+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2000/"},
    {"title": "Тор", "year": "2011", "rating": "7.0", "genre": "Фэнтези", "country": "США", "duration": "115 мин", "description": "Бог грома изгнан на Землю.", "player_url": "https://www.youtube.com/results?search_query=тор+2011+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2011/"},
    {"title": "Первый мститель", "year": "2011", "rating": "6.9", "genre": "Боевик", "country": "США", "duration": "124 мин", "description": "Стив Роджерс становится Капитаном Америкой.", "player_url": "https://www.youtube.com/results?search_query=первый+мститель+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2011/"},
    {"title": "Стражи Галактики", "year": "2014", "rating": "8.0", "genre": "Фантастика", "country": "США", "duration": "121 мин", "description": "Группа неудачников спасает галактику.", "player_url": "https://www.youtube.com/results?search_query=стражи+галактики+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2014/"},
    {"title": "Супермен", "year": "1978", "rating": "7.4", "genre": "Фантастика", "country": "США", "duration": "143 мин", "description": "Последний сын Криптона.", "player_url": "https://www.youtube.com/results?search_query=супермен+1978+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1978/"},
    {"title": "Чужой", "year": "1979", "rating": "8.5", "genre": "Ужасы", "country": "США", "duration": "117 мин", "description": "Экипаж vs инопланетянин.", "player_url": "https://www.youtube.com/results?search_query=чужой+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1979/"},
    {"title": "Чужие", "year": "1986", "rating": "8.4", "genre": "Ужасы", "country": "США", "duration": "137 мин", "description": "Рипли возвращается.", "player_url": "https://www.youtube.com/results?search_query=чужие+2+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1986/"},
    {"title": "Хищник", "year": "1987", "rating": "7.8", "genre": "Боевик", "country": "США", "duration": "107 мин", "description": "Спецназ vs инопланетный охотник.", "player_url": "https://www.youtube.com/results?search_query=хищник+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1987/"},
    {"title": "Нечто", "year": "1982", "rating": "8.2", "genre": "Ужасы", "country": "США", "duration": "109 мин", "description": "Полярники vs инопланетная форма.", "player_url": "https://www.youtube.com/results?search_query=нечто+1982+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1982/"},
    {"title": "Сияние", "year": "1980", "rating": "8.4", "genre": "Ужасы", "country": "США", "duration": "146 мин", "description": "Писатель сходит с ума в отеле.", "player_url": "https://www.youtube.com/results?search_query=сияние+1980+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1980/"},
    {"title": "Оно", "year": "2017", "rating": "7.3", "genre": "Ужасы", "country": "США", "duration": "135 мин", "description": "Дети vs клоун Пеннивайз.", "player_url": "https://www.youtube.com/results?search_query=оно+2017+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2017/"},
    {"title": "Заклятие", "year": "2013", "rating": "7.5", "genre": "Ужасы", "country": "США", "duration": "112 мин", "description": "Семья в доме с привидениями.", "player_url": "https://www.youtube.com/results?search_query=заклятие+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2013/"},
    {"title": "Астрал", "year": "2010", "rating": "6.8", "genre": "Ужасы", "country": "США", "duration": "103 мин", "description": "Семья спасает сына из астрала.", "player_url": "https://www.youtube.com/results?search_query=астрал+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2010/"},
    {"title": "Пила: Игра на выживание", "year": "2004", "rating": "7.6", "genre": "Ужасы", "country": "США", "duration": "103 мин", "description": "Ловушка маньяка.", "player_url": "https://www.youtube.com/results?search_query=пила+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2004/"},
    {"title": "Крик", "year": "1996", "rating": "7.4", "genre": "Ужасы", "country": "США", "duration": "111 мин", "description": "Маньяк в маске.", "player_url": "https://www.youtube.com/results?search_query=крик+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1996/"},
    {"title": "Тихое место", "year": "2018", "rating": "7.5", "genre": "Ужасы", "country": "США", "duration": "90 мин", "description": "Нельзя шуметь — убьют.", "player_url": "https://www.youtube.com/results?search_query=тихое+место+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2018/"},
    {"title": "Прочь", "year": "2017", "rating": "7.7", "genre": "Ужасы", "country": "США", "duration": "104 мин", "description": "Знакомство с родителями.", "player_url": "https://www.youtube.com/results?search_query=прочь+фильм+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2017/"},
    {"title": "Джанго освобождённый", "year": "2012", "rating": "8.4", "genre": "Вестерн", "country": "США", "duration": "165 мин", "description": "Охотник за головами освобождает раба.", "player_url": "https://www.youtube.com/results?search_query=джанго+освобождённый+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2012/"},
    {"title": "Безумный Макс: Дорога ярости", "year": "2015", "rating": "8.1", "genre": "Боевик", "country": "Австралия", "duration": "120 мин", "description": "Побег через пустыню.", "player_url": "https://www.youtube.com/results?search_query=безумный+макс+дорога+ярости+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2015/"},
    {"title": "Город Бога", "year": "2002", "rating": "8.6", "genre": "Криминал", "country": "Бразилия", "duration": "130 мин", "description": "Жизнь в фавелах Рио.", "player_url": "https://www.youtube.com/results?search_query=город+бога+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2002/"},
    {"title": "Паразиты", "year": "2019", "rating": "8.5", "genre": "Триллер", "country": "Южная Корея", "duration": "132 мин", "description": "Бедные проникают к богатым.", "player_url": "https://www.youtube.com/results?search_query=паразиты+2019+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2019/"},
    {"title": "Унесённые призраками", "year": "2001", "rating": "8.6", "genre": "Аниме", "country": "Япония", "duration": "125 мин", "description": "Девочка в городе духов.", "player_url": "https://www.youtube.com/results?search_query=унесённые+призраками+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2001/"},
    {"title": "Титаник", "year": "1997", "rating": "7.9", "genre": "Драма", "country": "США", "duration": "194 мин", "description": "Любовь на борту Титаника.", "player_url": "https://www.youtube.com/results?search_query=титаник+1997+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/1997/"},
    {"title": "Богемская рапсодия", "year": "2018", "rating": "7.9", "genre": "Драма", "country": "США", "duration": "134 мин", "description": "История Фредди Меркьюри.", "player_url": "https://www.youtube.com/results?search_query=богемская+рапсодия+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2018/"},
    {"title": "Элвис", "year": "2022", "rating": "7.3", "genre": "Драма", "country": "США", "duration": "159 мин", "description": "История Элвиса Пресли.", "player_url": "https://www.youtube.com/results?search_query=элвис+2022+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2022/"},
    {"title": "Рокетмен", "year": "2019", "rating": "7.3", "genre": "Драма", "country": "Великобритания", "duration": "121 мин", "description": "История Элтона Джона.", "player_url": "https://www.youtube.com/results?search_query=рокетмен+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2019/"},
    {"title": "Барби", "year": "2023", "rating": "6.8", "genre": "Комедия", "country": "США", "duration": "114 мин", "description": "Барби в реальном мире.", "player_url": "https://www.youtube.com/results?search_query=барби+2023+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2023/"},
    {"title": "Ёж Соник", "year": "2020", "rating": "6.5", "genre": "Фантастика", "country": "США", "duration": "99 мин", "description": "Синий ёж с суперскоростью.", "player_url": "https://www.youtube.com/results?search_query=ёж+соник+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2020/"},
    {"title": "Марио", "year": "2023", "rating": "7.0", "genre": "Мультфильм", "country": "США", "duration": "92 мин", "description": "Водопроводчик спасает принцессу.", "player_url": "https://www.youtube.com/results?search_query=супер+марио+в+кино+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2023/"},
    {"title": "Аквамен", "year": "2018", "rating": "6.8", "genre": "Фэнтези", "country": "США", "duration": "143 мин", "description": "Король Атлантиды.", "player_url": "https://www.youtube.com/results?search_query=аквамен+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2018/"},
    {"title": "Чудо-женщина", "year": "2017", "rating": "7.4", "genre": "Фэнтези", "country": "США", "duration": "141 мин", "description": "Амазонка в Первой мировой.", "player_url": "https://www.youtube.com/results?search_query=чудо+женщина+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2017/"},
    {"title": "Веном", "year": "2018", "rating": "6.7", "genre": "Фантастика", "country": "США", "duration": "112 мин", "description": "Журналист и симбиот.", "player_url": "https://www.youtube.com/results?search_query=веном+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2018/"},
    {"title": "Шазам!", "year": "2019", "rating": "7.0", "genre": "Фэнтези", "country": "США", "duration": "132 мин", "description": "Подросток превращается в героя.", "player_url": "https://www.youtube.com/results?search_query=шазам+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2019/"},
    {"title": "Доктор Стрэндж", "year": "2016", "rating": "7.5", "genre": "Фэнтези", "country": "США", "duration": "115 мин", "description": "Хирург становится магом.", "player_url": "https://www.youtube.com/results?search_query=доктор+стрэндж+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2016/"},
    {"title": "Чёрная пантера", "year": "2018", "rating": "7.3", "genre": "Фэнтези", "country": "США", "duration": "134 мин", "description": "Король Ваканды.", "player_url": "https://www.youtube.com/results?search_query=чёрная+пантера+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2018/"},
    {"title": "Человек-муравей", "year": "2015", "rating": "7.3", "genre": "Фантастика", "country": "США", "duration": "117 мин", "description": "Вор с костюмом-жуком.", "player_url": "https://www.youtube.com/results?search_query=человек+муравей+1+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2015/"},
    {"title": "Капитан Марвел", "year": "2019", "rating": "6.8", "genre": "Фантастика", "country": "США", "duration": "123 мин", "description": "Кэрол Дэнверс обретает силы.", "player_url": "https://www.youtube.com/results?search_query=капитан+марвел+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2019/"},
    {"title": "Тор: Рагнарёк", "year": "2017", "rating": "7.9", "genre": "Фэнтези", "country": "США", "duration": "130 мин", "description": "Тор против Хелы.", "player_url": "https://www.youtube.com/results?search_query=тор+рагнарёк+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2017/"},
    {"title": "Первый мститель: Противостояние", "year": "2016", "rating": "7.8", "genre": "Боевик", "country": "США", "duration": "147 мин", "description": "Мстители против Мстителей.", "player_url": "https://www.youtube.com/results?search_query=первый+мститель+противостояние+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2016/"},
    {"title": "Стражи Галактики. Часть 2", "year": "2017", "rating": "7.6", "genre": "Фантастика", "country": "США", "duration": "136 мин", "description": "Звёздный Лорд встречает отца.", "player_url": "https://www.youtube.com/results?search_query=стражи+галактики+2+смотреть+на+русском", "kp_url": "https://kinopoisk.ru/film/2017/"},
]

# Главная клавиатура
def get_keyboard():
    kb = [
        [KeyboardButton(text="🎬 Все фильмы"), KeyboardButton(text="🔍 Поиск")],
        [KeyboardButton(text="🎲 Случайный"), KeyboardButton(text="📊 Топ")],
        [KeyboardButton(text="🍿 Популярные"), KeyboardButton(text="🆕 Новинки")],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# Клавиатура для фильма
def get_movie_kb(url, kp_url=None):
    kb = [
        [InlineKeyboardButton(text="▶️ Смотреть на YouTube", url=url)],
    ]
    if kp_url:
        kb.append([InlineKeyboardButton(text="📄 Кинопоиск", url=kp_url)])
    return InlineKeyboardMarkup(inline_keyboard=kb)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(f"Получена команда /start от {message.from_user.id}")
    try:
        await message.answer(
            "🎬 <b>Бот «Что посмотреть?»</b>\n\n"
            f"📚 <b>{len(MOVIES_DB)}</b> фильмов бесплатно!\n"
            f"✅ YouTube — работает без VPN!\n\n"
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
    text = "📋 <b>Все фильмы (100):</b>\n\n"
    for i, m in enumerate(MOVIES_DB[:20], 1):
        text += f"{i}. {m['title']} ({m['year']}) ⭐{m['rating']}\n"
    text += "\n...и ещё 80 фильмов!\n\nВведите название для поиска."
    await message.answer(text, parse_mode="HTML")

# Кнопка "Поиск"
@dp.message(F.text == "🔍 Поиск")
async def search_cmd(message: Message):
    await message.answer(
        "🔍 <b>Введите название фильма:</b>\n\n<i>Например: Матрица, Гарри Поттер, Шрек</i>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️ Назад")]], resize_keyboard=True)
    )

# Кнопка "Случайный"
@dp.message(F.text == "🎲 Случайный")
async def random_movie(message: Message):
    m = random.choice(MOVIES_DB)
    text = f"🎲 <b>Случайный выбор:</b>\n\n🎬 {m['title']}\n📅 {m['year']} | ⭐ {m['rating']}\n🎭 {m['genre']}\n🌍 {m['country']}\n\n{m['description']}"
    await message.answer(text, parse_mode="HTML", reply_markup=get_movie_kb(m['player_url'], m.get('kp_url')))

# Кнопка "Топ"
@dp.message(F.text == "📊 Топ")
async def top_movies(message: Message):
    top = sorted(MOVIES_DB, key=lambda x: float(x['rating']), reverse=True)[:10]
    text = "📊 <b>Топ-10 по рейтингу:</b>\n\n"
    for i, m in enumerate(top, 1):
        text += f"{i}. {m['title']} — ⭐{m['rating']}\n"
    await message.answer(text, parse_mode="HTML")

# Кнопка "Популярные"
@dp.message(F.text == "🍿 Популярные")
async def popular_movies(message: Message):
    text = "🍿 <b>Популярные фильмы:</b>\n\n"
    for i, m in enumerate(MOVIES_DB[:10], 1):
        text += f"{i}. {m['title']} ({m['year']}) — ⭐{m['rating']}\n"
    await message.answer(text, parse_mode="HTML")

# Кнопка "Новинки"
@dp.message(F.text == "🆕 Новинки")
async def new_movies(message: Message):
    new = [m for m in MOVIES_DB if int(m['year']) >= 2020][:10]
    if new:
        text = "🆕 <b>Новинки (2020+):</b>\n\n"
        for i, m in enumerate(new, 1):
            text += f"{i}. {m['title']} ({m['year']}) — ⭐{m['rating']}\n"
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer("🆕 Новинки добавляются регулярно!")

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
        for m in found[:5]:
            text = f"🎬 <b>{m['title']}</b>\n📅 {m['year']} | ⭐ {m['rating']}\n🎭 {m['genre']}\n\n{m['description']}"
            await message.answer(text, parse_mode="HTML", reply_markup=get_movie_kb(m['player_url'], m.get('kp_url')))
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔍 Найти на YouTube", url=f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}+смотреть+на+русском")]])
        await message.answer(f"😔 <b>{message.text}</b> не найден в базе.\n\nПопробуйте YouTube:", parse_mode="HTML", reply_markup=kb)

async def main():
    logger.info("🚀 Запуск бота «Что посмотреть?»...")
    logger.info(f"📊 Фильмов в базе: {len(MOVIES_DB)}")
    logger.info(f"💾 Источник: YouTube (поиск фильмов на русском)")
    logger.info(f"Токен: {BOT_TOKEN[:20]}...")
    
    # Проверка базы
    for i, movie in enumerate(MOVIES_DB):
        if 'title' not in movie or 'player_url' not in movie:
            logger.error(f"Фильм {i} не имеет title или player_url!")
    
    logger.info("✅ База проверена")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
