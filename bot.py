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

# 🔥 БАЗА ИЗ 100 ФИЛЬМОВ 🔥
MOVIES_DB = [
    {"title": "Побег из Шоушенка", "year": "1994", "rating": "9.3", "genre": "Драма", "country": "США", "duration": "142 мин", "description": "Бухгалтер обвинён в убийстве жены. В тюрьме он находит друзей и надежду.", "player_url": "https://rutube.ru/video/search/побег+из+шоушенка", "source": "RuTube"},
    {"title": "Зелёная миля", "year": "1999", "rating": "9.2", "genre": "Драма / Фэнтези", "country": "США", "duration": "189 мин", "description": "Начальник блока смертников встречает заключённого с даром исцеления.", "player_url": "https://rutube.ru/video/search/зелёная+миля", "source": "RuTube"},
    {"title": "Крёстный отец", "year": "1972", "rating": "9.2", "genre": "Криминал / Драма", "country": "США", "duration": "175 мин", "description": "Сага о мафиозной семье Корлеоне и борьбе за власть.", "player_url": "https://rutube.ru/video/search/крёстный+отец", "source": "RuTube"},
    {"title": "Тёмный рыцарь", "year": "2008", "rating": "9.0", "genre": "Боевик / Драма", "country": "США", "duration": "152 мин", "description": "Бэтмен противостоит Джокеру, сеющему хаос в Готэме.", "player_url": "https://rutube.ru/video/search/тёмный+рыцарь", "source": "RuTube"},
    {"title": "Список Шиндлера", "year": "1993", "rating": "9.0", "genre": "Драма / Биография", "country": "США", "duration": "195 мин", "description": "История Оскара Шиндлера, спасшего более тысячи евреев во время Холокоста.", "player_url": "https://rutube.ru/video/search/список+шиндлера", "source": "RuTube"},
    {"title": "1+1 (Неприкасаемые)", "year": "2011", "rating": "8.9", "genre": "Комедия / Драма", "country": "Франция", "duration": "112 мин", "description": "Аристократ в инвалидном кресле и парень с улицы становятся друзьями.", "player_url": "https://rutube.ru/video/search/1+1+неприкасаемые", "source": "RuTube"},
    {"title": "Криминальное чтиво", "year": "1994", "rating": "8.9", "genre": "Криминал / Драма", "country": "США", "duration": "154 мин", "description": "Культовый фильм Тарантино о криминальном мире Лос-Анджелеса.", "player_url": "https://rutube.ru/video/search/криминальное+чтиво", "source": "RuTube"},
    {"title": "Начало", "year": "2010", "rating": "8.8", "genre": "Боевик / Фантастика", "country": "США", "duration": "148 мин", "description": "Вор, крадущий секреты из снов, получает задание внедрить идею.", "player_url": "https://rutube.ru/video/search/начало+фильм+2010", "source": "RuTube"},
    {"title": "Властелин колец: Братство Кольца", "year": "2001", "rating": "8.8", "genre": "Фэнтези / Приключения", "country": "Новая Зеландия", "duration": "178 мин", "description": "Фродо отправляется уничтожить Кольцо Всевластия.", "player_url": "https://rutube.ru/video/search/властелин+колец+1", "source": "RuTube"},
    {"title": "Форрест Гамп", "year": "1994", "rating": "8.8", "genre": "Драма / Комедия", "country": "США", "duration": "142 мин", "description": "Простой парень с большим сердцем становится участником великих событий.", "player_url": "https://rutube.ru/video/search/форрест+гамп", "source": "RuTube"},
    {"title": "Бойцовский клуб", "year": "1999", "rating": "8.8", "genre": "Драма / Триллер", "country": "США", "duration": "139 мин", "description": "Клерк создаёт подпольный бойцовский клуб, который становится культом.", "player_url": "https://rutube.ru/video/search/бойцовский+клуб", "source": "RuTube"},
    {"title": "Матрица", "year": "1999", "rating": "8.7", "genre": "Боевик / Фантастика", "country": "США", "duration": "136 мин", "description": "Хакер узнаёт, что мир — симуляция. Ему предстоит выбрать правду.", "player_url": "https://rutube.ru/video/search/матрица+1", "source": "RuTube"},
    {"title": "Интерстеллар", "year": "2014", "rating": "8.7", "genre": "Фантастика / Драма", "country": "США", "duration": "169 мин", "description": "Экспедиция через червоточину в поисках нового дома для человечества.", "player_url": "https://rutube.ru/video/search/интерстеллар", "source": "RuTube"},
    {"title": "Леон", "year": "1994", "rating": "8.7", "genre": "Боевик / Драма", "country": "Франция", "duration": "133 мин", "description": "Киллер приютил девочку, чью семью убили полицейские.", "player_url": "https://rutube.ru/video/search/леон+фильм", "source": "RuTube"},
    {"title": "Назад в будущее", "year": "1985", "rating": "8.7", "genre": "Фантастика / Комедия", "country": "США", "duration": "116 мин", "description": "Подросток отправляется в прошлое на машине времени.", "player_url": "https://rutube.ru/video/search/назад+в+будущее+1", "source": "RuTube"},
    {"title": "Унесённые призраками", "year": "2001", "rating": "8.6", "genre": "Аниме / Фэнтези", "country": "Япония", "duration": "125 мин", "description": "Девочка попадает в город духов и должна спасти родителей.", "player_url": "https://rutube.ru/video/search/унесённые+призраками", "source": "RuTube"},
    {"title": "Паразиты", "year": "2019", "rating": "8.5", "genre": "Драма / Триллер", "country": "Южная Корея", "duration": "132 мин", "description": "Бедная семья хитростью проникает в дом богатых.", "player_url": "https://rutube.ru/video/search/паразиты+2019", "source": "RuTube"},
    {"title": "Джокер", "year": "2019", "rating": "8.4", "genre": "Триллер / Драма", "country": "США", "duration": "122 мин", "description": "История происхождения главного врага Бэтмена.", "player_url": "https://rutube.ru/video/search/джокер+2019", "source": "RuTube"},
    {"title": "Мстители: Финал", "year": "2019", "rating": "8.2", "genre": "Боевик / Фантастика", "country": "США", "duration": "181 мин", "description": "Мстители собираются в последний раз для битвы с Таносом.", "player_url": "https://rutube.ru/video/search/мстители+финал", "source": "RuTube"},
    {"title": "Гарри Поттер и философский камень", "year": "2001", "rating": "7.6", "genre": "Фэнтези / Приключения", "country": "Великобритания", "duration": "152 мин", "description": "Мальчик-сирота узнаёт, что он волшебник, и едет в Хогвартс.", "player_url": "https://rutube.ru/video/search/гарри+поттер+1", "source": "RuTube"},
    {"title": "Властелин колец: Две крепости", "year": "2002", "rating": "8.7", "genre": "Фэнтези / Приключения", "country": "Новая Зеландия", "duration": "179 мин", "description": "Братство распалось. Фродо и Сэм продолжают путь к Роковой горе.", "player_url": "https://rutube.ru/video/search/властелин+колец+2", "source": "RuTube"},
    {"title": "Властелин колец: Возвращение короля", "year": "2003", "rating": "8.9", "genre": "Фэнтези / Приключения", "country": "Новая Зеландия", "duration": "201 мин", "description": "Финальная битва за Средиземье. Фродо достигает цели.", "player_url": "https://rutube.ru/video/search/властелин+колец+3", "source": "RuTube"},
    {"title": "Хороший, плохой, злой", "year": "1966", "rating": "8.8", "genre": "Вестерн", "country": "Италия", "duration": "178 мин", "description": "Три охотника за сокровищами в погоне за золотом конфедератов.", "player_url": "https://rutube.ru/video/search/хороший+плохой+злой", "source": "RuTube"},
    {"title": "Спасти рядового Райана", "year": "1998", "rating": "8.6", "genre": "Военный / Драма", "country": "США", "duration": "169 мин", "description": "Отряд солдат отправляется на поиски рядового Райана во время Второй мировой.", "player_url": "https://rutube.ru/video/search/спасти+рядового+райана", "source": "RuTube"},
    {"title": "Молчание ягнят", "year": "1991", "rating": "8.6", "genre": "Триллер / Криминал", "country": "США", "duration": "118 мин", "description": "Агент ФБР просит помощи у каннибала Ганнибала Лектера.", "player_url": "https://rutube.ru/video/search/молчание+ягнят", "source": "RuTube"},
    {"title": "Гладиатор", "year": "2000", "rating": "8.5", "genre": "Боевик / Драма", "country": "США", "duration": "155 мин", "description": "Римский генерал становится гладиатором и мстит императору.", "player_url": "https://rutube.ru/video/search/гладиатор+2000", "source": "RuTube"},
    {"title": "Терминатор 2: Судный день", "year": "1991", "rating": "8.5", "genre": "Боевик / Фантастика", "country": "США", "duration": "137 мин", "description": "Терминатор защищает Джона Коннора от жидкого металла.", "player_url": "https://rutube.ru/video/search/терминатор+2", "source": "RuTube"},
    {"title": "Назад в будущее 2", "year": "1989", "rating": "8.5", "genre": "Фантастика / Комедия", "country": "США", "duration": "108 мин", "description": "Марти и Док отправляются в будущее, чтобы исправить ошибку.", "player_url": "https://rutube.ru/video/search/назад+в+будущее+2", "source": "RuTube"},
    {"title": "Город Бога", "year": "2002", "rating": "8.6", "genre": "Криминал / Драма", "country": "Бразилия", "duration": "130 мин", "description": "История жизни в фавелах Рио-де-Жанейро через судьбы двух парней.", "player_url": "https://rutube.ru/video/search/город+бога", "source": "RuTube"},
    {"title": "Семь", "year": "1995", "rating": "8.6", "genre": "Триллер / Криминал", "country": "США", "duration": "127 мин", "description": "Два детектива ищут маньяка, убивающего по семи смертным грехам.", "player_url": "https://rutube.ru/video/search/семь+фильм+1995", "source": "RuTube"},
    {"title": "Жизнь прекрасна", "year": "1997", "rating": "8.6", "genre": "Драма / Комедия", "country": "Италия", "duration": "116 мин", "description": "Отец защищает сына от ужасов концлагеря, превращая всё в игру.", "player_url": "https://rutube.ru/video/search/жизнь+прекрасна", "source": "RuTube"},
    {"title": "Звёздные войны: Эпизод 5", "year": "1980", "rating": "8.7", "genre": "Фантастика / Приключения", "country": "США", "duration": "124 мин", "description": "Люк Скайуокер обучается у Йоды. Вейдер раскрывает тайну Люку.", "player_url": "https://rutube.ru/video/search/звёздные+войны+5", "source": "RuTube"},
    {"title": "Матрица: Перезагрузка", "year": "2003", "rating": "7.2", "genre": "Боевик / Фантастика", "country": "США", "duration": "138 мин", "description": "Нео продолжает борьбу с машинами и узнаёт правду о Матрице.", "player_url": "https://rutube.ru/video/search/матрица+2", "source": "RuTube"},
    {"title": "Матрица: Революция", "year": "2003", "rating": "6.8", "genre": "Боевик / Фантастика", "country": "США", "duration": "129 мин", "description": "Финальная битва Нео со Смитом и машинами.", "player_url": "https://rutube.ru/video/search/матрица+3", "source": "RuTube"},
    {"title": "Гарри Поттер и Тайная комната", "year": "2002", "rating": "7.7", "genre": "Фэнтези / Приключения", "country": "Великобритания", "duration": "161 мин", "description": "Гарри возвращается в Хогвартс и сталкивается с наследником Слизерина.", "player_url": "https://rutube.ru/video/search/гарри+поттер+2", "source": "RuTube"},
    {"title": "Гарри Поттер и узник Азкабана", "year": "2004", "rating": "7.9", "genre": "Фэнтези / Приключения", "country": "Великобритания", "duration": "142 мин", "description": "Гарри узнаёт правду о Сириусе Блэке и своих родителях.", "player_url": "https://rutube.ru/video/search/гарри+поттер+3", "source": "RuTube"},
    {"title": "Убить пересмешника", "year": "1962", "rating": "8.3", "genre": "Драма", "country": "США", "duration": "129 мин", "description": "Адвокат защищает чернокожего в расистском городке на Юге США.", "player_url": "https://rutube.ru/video/search/убить+пересмешника", "source": "RuTube"},
    {"title": "Безумный Макс: Дорога ярости", "year": "2015", "rating": "8.1", "genre": "Боевик / Приключения", "country": "Австралия", "duration": "120 мин", "description": "Макс и Фуриоса бегут от тирана через постапокалиптическую пустыню.", "player_url": "https://rutube.ru/video/search/безумный+макс+4", "source": "RuTube"},
    {"title": "Джанго освобождённый", "year": "2012", "rating": "8.4", "genre": "Вестерн / Драма", "country": "США", "duration": "165 мин", "description": "Охотник за головами помогает рабу освободить жену.", "player_url": "https://rutube.ru/video/search/джанго+освобождённый", "source": "RuTube"},
    {"title": "ВАЛЛ·И", "year": "2008", "rating": "8.4", "genre": "Мультфильм / Фантастика", "country": "США", "duration": "98 мин", "description": "Последний робот на Земле влюбляется и спасает человечество.", "player_url": "https://rutube.ru/video/search/валл-и", "source": "RuTube"},
    {"title": "Вверх", "year": "2009", "rating": "8.2", "genre": "Мультфильм / Приключения", "country": "США", "duration": "96 мин", "description": "Старик и мальчик летят на доме с шарами в Южную Америку.", "player_url": "https://rutube.ru/video/search/вверх+мультфильм", "source": "RuTube"},
    {"title": "Тайна Коко", "year": "2017", "rating": "8.4", "genre": "Мультфильм / Фэнтези", "country": "США", "duration": "105 мин", "description": "Мальчик попадает в страну мёртвых и ищет своего прадеда.", "player_url": "https://rutube.ru/video/search/тайна+коко", "source": "RuTube"},
    {"title": "Король Лев", "year": "1994", "rating": "8.5", "genre": "Мультфильм / Драма", "country": "США", "duration": "88 мин", "description": "Львёнок Симба должен вернуть трон после смерти отца.", "player_url": "https://rutube.ru/video/search/король+лев+1994", "source": "RuTube"},
    {"title": "Титаник", "year": "1997", "rating": "7.9", "genre": "Драма / Мелодрама", "country": "США", "duration": "194 мин", "description": "Любовь аристократки и бедного художника на борту Титаника.", "player_url": "https://rutube.ru/video/search/титаник+1997", "source": "RuTube"},
    {"title": "Аватар", "year": "2009", "rating": "7.9", "genre": "Фантастика / Приключения", "country": "США", "duration": "162 мин", "description": "Парализованный солдат попадает на Пандору и становится частью народа На'ви.", "player_url": "https://rutube.ru/video/search/аватар+2009", "source": "RuTube"},
    {"title": "День сурка", "year": "1993", "rating": "8.0", "genre": "Комедия / Фэнтези", "country": "США", "duration": "101 мин", "description": "Телеведущий проживает один и тот же день снова и снова.", "player_url": "https://rutube.ru/video/search/день+сурка", "source": "RuTube"},
    {"title": "Один дома", "year": "1990", "rating": "7.7", "genre": "Комедия / Семейный", "country": "США", "duration": "103 мин", "description": "Мальчик остаётся один дома и защищает его от грабителей.", "player_url": "https://rutube.ru/video/search/один+дома+1", "source": "RuTube"},
    {"title": "Один дома 2: Затерянный в Нью-Йорке", "year": "1992", "rating": "7.2", "genre": "Комедия / Семейный", "country": "США", "duration": "120 мин", "description": "Кевин попадает в Нью-Йорк один и снова сражается с бандитами.", "player_url": "https://rutube.ru/video/search/один+дома+2", "source": "RuTube"},
    {"title": "Маска", "year": "1994", "rating": "6.9", "genre": "Комедия / Фэнтези", "country": "США", "duration": "101 мин", "description": "Скромный клерк находит магическую маску, превращающую его в супергероя.", "player_url": "https://rutube.ru/video/search/маска+1994", "source": "RuTube"},
    {"title": "Мальчишник в Вегасе", "year": "2009", "rating": "7.7", "genre": "Комедия", "country": "США", "duration": "100 мин", "description": "Друзья просыпаются после мальчишника и не помнят, где жених.", "player_url": "https://rutube.ru/video/search/мальчишник+в+вегасе", "source": "RuTube"},
    {"title": "Амели", "year": "2001", "rating": "8.3", "genre": "Комедия / Мелодрама", "country": "Франция", "duration": "122 мин", "description": "Девушка меняет жизни людей к лучшему, оставаясь в тени.", "player_url": "https://rutube.ru/video/search/амели", "source": "RuTube"},
    {"title": "Такси", "year": "1998", "rating": "7.0", "genre": "Боевик / Комедия", "country": "Франция", "duration": "86 мин", "description": "Таксист и полицейский ловят банду грабителей банков.", "player_url": "https://rutube.ru/video/search/такси+1998", "source": "RuTube"},
    {"title": "Перевозчик", "year": "2002", "rating": "6.8", "genre": "Боевик / Криминал", "country": "Франция", "duration": "92 мин", "description": "Профессиональный курьер нарушает правила ради спасения девушки.", "player_url": "https://rutube.ru/video/search/перевозчик+1", "source": "RuTube"},
    {"title": "Миссия невыполнима", "year": "1996", "rating": "7.2", "genre": "Боевик / Триллер", "country": "США", "duration": "110 мин", "description": "Итан Хант очищает своё имя после провала миссии.", "player_url": "https://rutube.ru/video/search/миссия+невыполнима+1", "source": "RuTube"},
    {"title": "Крепкий орешек", "year": "1988", "rating": "8.2", "genre": "Боевик / Триллер", "country": "США", "duration": "132 мин", "description": "Полицейский один противостоит террористам в небоскрёбе.", "player_url": "https://rutube.ru/video/search/крепкий+орешек+1", "source": "RuTube"},
    {"title": "Рэмбо: Первая кровь", "year": "1982", "rating": "7.7", "genre": "Боевик / Приключения", "country": "США", "duration": "93 мин", "description": "Ветеран Вьетнама сражается с полицией маленького городка.", "player_url": "https://rutube.ru/video/search/рэмбо+1", "source": "RuTube"},
    {"title": "Рокки", "year": "1976", "rating": "8.1", "genre": "Драма / Спорт", "country": "США", "duration": "120 мин", "description": "Неизвестный боксёр получает шанс сразиться с чемпионом.", "player_url": "https://rutube.ru/video/search/рокки+1", "source": "RuTube"},
    {"title": "Трансформеры", "year": "2007", "rating": "7.0", "genre": "Боевик / Фантастика", "country": "США", "duration": "144 мин", "description": "Автоботы и десептиконы сражаются на Земле за Куб.", "player_url": "https://rutube.ru/video/search/трансформеры+1", "source": "RuTube"},
    {"title": "Пираты Карибского моря: Проклятие Чёрной жемчужины", "year": "2003", "rating": "8.0", "genre": "Приключения / Фэнтези", "country": "США", "duration": "143 мин", "description": "Джек Воробей и Уилл Тернер спасают Элизабет от проклятых пиратов.", "player_url": "https://rutube.ru/video/search/пираты+карибского+моря+1", "source": "RuTube"},
    {"title": "Индиана Джонс: В поисках утраченного ковчега", "year": "1981", "rating": "8.4", "genre": "Приключения / Боевик", "country": "США", "duration": "115 мин", "description": "Индиана Джонс ищет Ковчег Завета раньше нацистов.", "player_url": "https://rutube.ru/video/search/индиана+джонс+1", "source": "RuTube"},
    {"title": "Парк юрского периода", "year": "1993", "rating": "8.2", "genre": "Приключения / Фантастика", "country": "США", "duration": "127 мин", "description": "Динозавры вырываются на свободу в парке развлечений.", "player_url": "https://rutube.ru/video/search/парк+юрского+периода+1", "source": "RuTube"},
    {"title": "Люди Икс", "year": "2000", "rating": "7.3", "genre": "Боевик / Фантастика", "country": "США", "duration": "104 мин", "description": "Мутанты сражаются за мирное сосуществование с людьми.", "player_url": "https://rutube.ru/video/search/люди+икс+1", "source": "RuTube"},
    {"title": "Железный человек", "year": "2008", "rating": "7.9", "genre": "Боевик / Фантастика", "country": "США", "duration": "126 мин", "description": "Тони Старк создаёт бронированный костюм и становится супергероем.", "player_url": "https://rutube.ru/video/search/железный+человек+1", "source": "RuTube"},
    {"title": "Тор", "year": "2011", "rating": "7.0", "genre": "Фэнтези / Боевик", "country": "США", "duration": "115 мин", "description": "Бог грома изгнан на Землю и должен стать достойным молота.", "player_url": "https://rutube.ru/video/search/тор+2011", "source": "RuTube"},
    {"title": "Первый мститель", "year": "2011", "rating": "6.9", "genre": "Боевик / Фантастика", "country": "США", "duration": "124 мин", "description": "Стив Роджерс становится Капитаном Америкой и сражается с Красным Черепом.", "player_url": "https://rutube.ru/video/search/первый+мститель", "source": "RuTube"},
    {"title": "Мстители", "year": "2012", "rating": "8.0", "genre": "Боевик / Фантастика", "country": "США", "duration": "143 мин", "description": "Герои Marvel объединяются против Локи и армии Читаури.", "player_url": "https://rutube.ru/video/search/мстители+2012", "source": "RuTube"},
    {"title": "Стражи Галактики", "year": "2014", "rating": "8.0", "genre": "Фантастика / Приключения", "country": "США", "duration": "121 мин", "description": "Группа неудачников спасает галактику от фанатика.", "player_url": "https://rutube.ru/video/search/стражи+галактики+1", "source": "RuTube"},
    {"title": "Человек-паук", "year": "2002", "rating": "7.4", "genre": "Боевик / Фантастика", "country": "США", "duration": "121 мин", "description": "Питер Паркер получает силы паука и становится супергероем.", "player_url": "https://rutube.ru/video/search/человек+паук+2002", "source": "RuTube"},
    {"title": "Бэтмен: Начало", "year": "2005", "rating": "8.2", "genre": "Боевик / Драма", "country": "США", "duration": "140 мин", "description": "История становления Брюса Уэйна Бэтменом.", "player_url": "https://rutube.ru/video/search/бэтмен+начало", "source": "RuTube"},
    {"title": "Супермен", "year": "1978", "rating": "7.4", "genre": "Фантастика / Приключения", "country": "США", "duration": "143 мин", "description": "Последний сын Криптона защищает Землю от Лекса Лютора.", "player_url": "https://rutube.ru/video/search/супермен+1978", "source": "RuTube"},
    {"title": "Хоббит: Нежданное путешествие", "year": "2012", "rating": "7.8", "genre": "Фэнтези / Приключения", "country": "Новая Зеландия", "duration": "169 мин", "description": "Бильбо Бэггинс отправляется в путешествие с гномами к Эребору.", "player_url": "https://rutube.ru/video/search/хоббит+1", "source": "RuTube"},
    {"title": "Хоббит: Пустошь Смауга", "year": "2013", "rating": "7.8", "genre": "Фэнтези / Приключения", "country": "Новая Зеландия", "duration": "161 мин", "description": "Гномы достигают Одинокой горы и сталкиваются со Смаугом.", "player_url": "https://rutube.ru/video/search/хоббит+2", "source": "RuTube"},
    {"title": "Хоббит: Битва пяти воинств", "year": "2014", "rating": "7.4", "genre": "Фэнтези / Приключения", "country": "Новая Зеландия", "duration": "144 мин", "description": "Гномы, эльфы и люди сражаются за Эребор.", "player_url": "https://rutube.ru/video/search/хоббит+3", "source": "RuTube"},
    {"title": "Гарри Поттер и Кубок огня", "year": "2005", "rating": "7.7", "genre": "Фэнтези / Приключения", "country": "Великобритания", "duration": "157 мин", "description": "Гарри участвует в Турнире Трёх Волшебников.", "player_url": "https://rutube.ru/video/search/гарри+поттер+4", "source": "RuTube"},
    {"title": "Гарри Поттер и Орден Феникса", "year": "2007", "rating": "7.5", "genre": "Фэнтези / Приключения", "country": "Великобритания", "duration": "138 мин", "description": "Гарри создаёт армию Дамблдора против Долорес Амбридж.", "player_url": "https://rutube.ru/video/search/гарри+поттер+5", "source": "RuTube"},
    {"title": "Гарри Поттер и Принц-полукровка", "year": "2009", "rating": "7.6", "genre": "Фэнтези / Приключения", "country": "Великобритания", "duration": "153 мин", "description": "Гарри узнаёт прошлое Волан-де-Морта. Дамблдор погибает.", "player_url": "https://rutube.ru/video/search/гарри+поттер+6", "source": "RuTube"},
    {"title": "Гарри Поттер и Дары Смерти: Часть 1", "year": "2010", "rating": "7.7", "genre": "Фэнтези / Приключения", "country": "Великобритания", "duration": "146 мин", "description": "Гарри, Рон и Гермиона ищут крестражи вне Хогвартса.", "player_url": "https://rutube.ru/video/search/гарри+поттер+7+часть+1", "source": "RuTube"},
    {"title": "Гарри Поттер и Дары Смерти: Часть 2", "year": "2011", "rating": "8.1", "genre": "Фэнтези / Приключения", "country": "Великобритания", "duration": "130 мин", "description": "Финальная битва за Хогвартс. Гарри противостоит Волан-де-Морту.", "player_url": "https://rutube.ru/video/search/гарри+поттер+7+часть+2", "source": "RuTube"},
    {"title": "Фантастические твари и где они обитают", "year": "2016", "rating": "7.2", "genre": "Фэнтези / Приключения", "country": "Великобритания", "duration": "132 мин", "description": "Ньют Саламандер прибывает в Нью-Йорк с магическими существами.", "player_url": "https://rutube.ru/video/search/фантастические+твари+1", "source": "RuTube"},
    {"title": "Мумия", "year": "1999", "rating": "7.1", "genre": "Приключения / Боевик", "country": "США", "duration": "124 мин", "description": "Археологи пробуждают древнеегипетского жреца Имхотепа.", "player_url": "https://rutube.ru/video/search/мумия+1999", "source": "RuTube"},
    {"title": "Голодные игры", "year": "2012", "rating": "7.2", "genre": "Фантастика / Приключения", "country": "США", "duration": "142 мин", "description": "Девушка добровольно участвует в смертельных играх вместо сестры.", "player_url": "https://rutube.ru/video/search/голодные+игры+1", "source": "RuTube"},
    {"title": "Голодные игры: И вспыхнет пламя", "year": "2013", "rating": "7.5", "genre": "Фантастика / Приключения", "country": "США", "duration": "146 мин", "description": "Китнисс и Пита отправляются на новые игры.", "player_url": "https://rutube.ru/video/search/голодные+игры+2", "source": "RuTube"},
    {"title": "Дивергент", "year": "2014", "rating": "6.6", "genre": "Фантастика / Приключения", "country": "США", "duration": "139 мин", "description": "Девушка узнаёт, что она дивергент и не вписывается в систему фракций.", "player_url": "https://rutube.ru/video/search/дивергент", "source": "RuTube"},
    {"title": "Бегущий в лабиринте", "year": "2014", "rating": "6.8", "genre": "Фантастика / Триллер", "country": "США", "duration": "113 мин", "description": "Парень просыпается в лифте без памяти и попадает в лабиринт.", "player_url": "https://rutube.ru/video/search/бегущий+в+лабиринте", "source": "RuTube"},
    {"title": "Довод", "year": "2020", "rating": "7.3", "genre": "Боевик / Фантастика", "country": "США", "duration": "150 мин", "description": "Агент манипулирует временем для предотвращения войны.", "player_url": "https://rutube.ru/video/search/довод+2020", "source": "RuTube"},
    {"title": "Дюна", "year": "2021", "rating": "8.0", "genre": "Фантастика / Приключения", "country": "США", "duration": "155 мин", "description": "Пол Атрейдес отправляется на Арракис за пряностью.", "player_url": "https://rutube.ru/video/search/дюна+2021", "source": "RuTube"},
    {"title": "Человек-паук: Через вселенные", "year": "2018", "rating": "8.4", "genre": "Мультфильм / Фантастика", "country": "США", "duration": "117 мин", "description": "Майлз Моралес становится Человеком-пауком в мультивселенной.", "player_url": "https://rutube.ru/video/search/человек+паук+через+вселенные", "source": "RuTube"},
    {"title": "Душа", "year": "2020", "rating": "8.0", "genre": "Мультфильм / Фэнтези", "country": "США", "duration": "100 мин", "description": "Учитель музыки попадает в мир душ и ищет смысл жизни.", "player_url": "https://rutube.ru/video/search/душа+мультфильм", "source": "RuTube"},
    {"title": "Холодное сердце", "year": "2013", "rating": "7.4", "genre": "Мультфильм / Мюзикл", "country": "США", "duration": "102 мин", "description": "Анна ищет сестру Эльзу, чтобы спасти королевство от вечной зимы.", "player_url": "https://rutube.ru/video/search/холодное+сердце", "source": "RuTube"},
    {"title": "Зверополис", "year": "2016", "rating": "8.0", "genre": "Мультфильм / Комедия", "country": "США", "duration": "108 мин", "description": "Кролик-полицейский и лис-мошенник раскрывают заговор.", "player_url": "https://rutube.ru/video/search/зверополис", "source": "RuTube"},
    {"title": "Гадкий я", "year": "2010", "rating": "7.6", "genre": "Мультфильм / Комедия", "country": "США", "duration": "95 мин", "description": "Суперзлодей усыновляет трёх сирот и встречает миньонов.", "player_url": "https://rutube.ru/video/search/гадкий+я+1", "source": "RuTube"},
    {"title": "Шрек", "year": "2001", "rating": "7.9", "genre": "Мультфильм / Комедия", "country": "США", "duration": "90 мин", "description": "Огр отправляется спасать принцессу для лорда Фаркуада.", "player_url": "https://rutube.ru/video/search/шрек+1", "source": "RuTube"},
    {"title": "Шрек 2", "year": "2004", "rating": "7.3", "genre": "Мультфильм / Комедия", "country": "США", "duration": "93 мин", "description": "Шрек и Фиона едут знакомиться с родителями.", "player_url": "https://rutube.ru/video/search/шрек+2", "source": "RuTube"},
    {"title": "Мадагаскар", "year": "2005", "rating": "6.9", "genre": "Мультфильм / Комедия", "country": "США", "duration": "86 мин", "description": "Животные из зоопарка попадают на Мадагаскар.", "player_url": "https://rutube.ru/video/search/мадагаскар+1", "source": "RuTube"},
    {"title": "Ледниковый период", "year": "2002", "rating": "7.5", "genre": "Мультфильм / Комедия", "country": "США", "duration": "81 мин", "description": "Мамонт, ленивец и саблезубый тигр возвращают ребёнка людям.", "player_url": "https://rutube.ru/video/search/ледниковый+период+1", "source": "RuTube"},
    {"title": "Как приручить дракона", "year": "2010", "rating": "8.1", "genre": "Мультфильм / Приключения", "country": "США", "duration": "98 мин", "description": "Викинг дружит с драконом Беззубиком.", "player_url": "https://rutube.ru/video/search/как+приручить+дракона+1", "source": "RuTube"},
    {"title": "Как приручить дракона 2", "year": "2014", "rating": "7.8", "genre": "Мультфильм / Приключения", "country": "США", "duration": "102 мин", "description": "Иккинг и Беззубик находят новую драконью стаю.", "player_url": "https://rutube.ru/video/search/как+приручить+дракона+2", "source": "RuTube"},
    {"title": "Как приручить дракона 3", "year": "2019", "rating": "8.1", "genre": "Мультфильм / Приключения", "country": "США", "duration": "104 мин", "description": "Иккинг ищет скрытый мир драконов.", "player_url": "https://rutube.ru/video/search/как+приручить+дракона+3", "source": "RuTube"},
    {"title": "История игрушек", "year": "1995", "rating": "8.3", "genre": "Мультфильм / Комедия", "country": "США", "duration": "81 мин", "description": "Ковбой Вуди и космический рейнджер Базз дружат.", "player_url": "https://rutube.ru/video/search/история+игрушек+1", "source": "RuTube"},
    {"title": "История игрушек 2", "year": "1999", "rating": "7.9", "genre": "Мультфильм / Комедия", "country": "США", "duration": "92 мин", "description": "Вуди похищен коллекционером, Базз спасает его.", "player_url": "https://rutube.ru/video/search/история+игрушек+2", "source": "RuTube"},
    {"title": "История игрушек: Большой побег", "year": "2010", "rating": "8.3", "genre": "Мультфильм / Комедия", "country": "США", "duration": "103 мин", "description": "Игрушки попадают в детский сад и планируют побег.", "player_url": "https://rutube.ru/video/search/история+игрушек+3", "source": "RuTube"},
    {"title": "В поисках Немо", "year": "2003", "rating": "8.2", "genre": "Мультфильм / Приключения", "country": "США", "duration": "100 мин", "description": "Рыбка-клоун ищет сына по всему океану.", "player_url": "https://rutube.ru/video/search/в+поисках+немо", "source": "RuTube"},
    {"title": "Рататуй", "year": "2007", "rating": "8.1", "genre": "Мультфильм / Комедия", "country": "США", "duration": "111 мин", "description": "Крыса мечтает стать шеф-поваром в Париже.", "player_url": "https://rutube.ru/video/search/рататуй", "source": "RuTube"},
    {"title": "Суперсемейка", "year": "2004", "rating": "8.0", "genre": "Мультфильм / Боевик", "country": "США", "duration": "115 мин", "description": "Семья супергероев выходит из подполья.", "player_url": "https://rutube.ru/video/search/суперсемейка+1", "source": "RuTube"},
    {"title": "Головоломка", "year": "2015", "rating": "8.1", "genre": "Мультфильм / Фэнтези", "country": "США", "duration": "95 мин", "description": "Эмоции управляют разумом девочки-подростка.", "player_url": "https://rutube.ru/video/search/головоломка", "source": "RuTube"},
    {"title": "Тачки", "year": "2006", "rating": "7.2", "genre": "Мультфильм / Комедия", "country": "США", "duration": "117 мин", "description": "Гоночная машина Молния Маккуин застревает в городке.", "player_url": "https://rutube.ru/video/search/тачки+1", "source": "RuTube"},
    {"title": "Мулан", "year": "1998", "rating": "7.7", "genre": "Мультфильм / Приключения", "country": "США", "duration": "88 мин", "description": "Девушка выдаёт себя за парня и идёт в армию вместо отца.", "player_url": "https://rutube.ru/video/search/мулан+1998", "source": "RuTube"},
    {"title": "Аладдин", "year": "1992", "rating": "8.0", "genre": "Мультфильм / Приключения", "country": "США", "duration": "90 мин", "description": "Уличный вор находит волшебную лампу с джинном.", "player_url": "https://rutube.ru/video/search/аладдин+1992", "source": "RuTube"},
    {"title": "Красавица и Чудовище", "year": "1991", "rating": "8.0", "genre": "Мультфильм / Мюзикл", "country": "США", "duration": "84 мин", "description": "Девушка живёт с заколдованным принцем-чудовищем.", "player_url": "https://rutube.ru/video/search/красавица+и+чудовище", "source": "RuTube"},
    {"title": "Корпорация монстров", "year": "2001", "rating": "8.1", "genre": "Мультфильм / Комедия", "country": "США", "duration": "92 мин", "description": "Монстры пугают детей для энергии, но встречают человеческую девочку.", "player_url": "https://rutube.ru/video/search/корпорация+монстров", "source": "RuTube"},
    {"title": "Рапунцель: Запутанная история", "year": "2010", "rating": "7.7", "genre": "Мультфильм / Мюзикл", "country": "США", "duration": "100 мин", "description": "Принцесса с длинными волосами сбегает из башни с вором.", "player_url": "https://rutube.ru/video/search/рапунцель", "source": "RuTube"},
    {"title": "Отряд самоубийц", "year": "2016", "rating": "5.9", "genre": "Боевик / Фантастика", "country": "США", "duration": "123 мин", "description": "Злодеи работают на правительство ради сокращения срока.", "player_url": "https://rutube.ru/video/search/отряд+самоубийц+1", "source": "RuTube"},
    {"title": "Отряд самоубийц 2", "year": "2021", "rating": "7.2", "genre": "Боевик / Фантастика", "country": "США", "duration": "132 мин", "description": "Новый отряд злодеев отправляется на миссию на остров.", "player_url": "https://rutube.ru/video/search/отряд+самоубийц+2", "source": "RuTube"},
    {"title": "Аквамен", "year": "2018", "rating": "6.8", "genre": "Фэнтези / Боевик", "country": "США", "duration": "143 мин", "description": "Артур Карри становится Акваменом и сражается за Атлантиду.", "player_url": "https://rutube.ru/video/search/аквамен", "source": "RuTube"},
    {"title": "Чудо-женщина", "year": "2017", "rating": "7.4", "genre": "Фэнтези / Боевик", "country": "США", "duration": "141 мин", "description": "Диана покидает остров амазонок и сражается в Первой мировой.", "player_url": "https://rutube.ru/video/search/чудо+женщина+1", "source": "RuTube"},
    {"title": "Бэтмен против Супермена", "year": "2016", "rating": "6.5", "genre": "Боевик / Фантастика", "country": "США", "duration": "151 мин", "description": "Бэтмен и Супермен сражаются, пока не появляется общий враг.", "player_url": "https://rutube.ru/video/search/бэтмен+против+супермена", "source": "RuTube"},
    {"title": "Лига справедливости", "year": "2017", "rating": "6.1", "genre": "Боевик / Фантастика", "country": "США", "duration": "120 мин", "description": "Герои DC объединяются против Степного Волка.", "player_url": "https://rutube.ru/video/search/лига+справедливости", "source": "RuTube"},
    {"title": "Хищник", "year": "1987", "rating": "7.8", "genre": "Боевик / Фантастика", "country": "США", "duration": "107 мин", "description": "Спецназовец сражается с инопланетным охотником в джунглях.", "player_url": "https://rutube.ru/video/search/хищник+1", "source": "RuTube"},
    {"title": "Чужой", "year": "1979", "rating": "8.5", "genre": "Ужасы / Фантастика", "country": "США", "duration": "117 мин", "description": "Экипаж корабля сталкивается с инопланетным организмом.", "player_url": "https://rutube.ru/video/search/чужой+1", "source": "RuTube"},
    {"title": "Чужие", "year": "1986", "rating": "8.4", "genre": "Ужасы / Боевик", "country": "США", "duration": "137 мин", "description": "Рипли возвращается на планету с колонией ксеноморфов.", "player_url": "https://rutube.ru/video/search/чужие+2", "source": "RuTube"},
    {"title": "Нечто", "year": "1982", "rating": "8.2", "genre": "Ужасы / Фантастика", "country": "США", "duration": "109 мин", "description": "Полярники сталкиваются с инопланетной формой жизни.", "player_url": "https://rutube.ru/video/search/нечто+1982", "source": "RuTube"},
    {"title": "Сияние", "year": "1980", "rating": "8.4", "genre": "Ужасы / Триллер", "country": "США", "duration": "146 мин", "description": "Писатель с семьёй зимует в отеле и сходит с ума.", "player_url": "https://rutube.ru/video/search/сияние+1980", "source": "RuTube"},
    {"title": "Оно", "year": "2017", "rating": "7.3", "genre": "Ужасы", "country": "США", "duration": "135 мин", "description": "Дети сражаются с клоуном-убийцей Пеннивайзом.", "player_url": "https://rutube.ru/video/search/оно+2017", "source": "RuTube"},
    {"title": "Заклятие", "year": "2013", "rating": "7.5", "genre": "Ужасы", "country": "США", "duration": "112 мин", "description": "Семья переезжает в дом с привидениями. Варрены расследуют.", "player_url": "https://rutube.ru/video/search/заклятие+1", "source": "RuTube"},
    {"title": "Прочь", "year": "2017", "rating": "7.7", "genre": "Ужасы / Триллер", "country": "США", "duration": "104 мин", "description": "Парень едет знакомиться с родителями девушки и попадает в ловушку.", "player_url": "https://rutube.ru/video/search/прочь+фильм", "source": "RuTube"},
    {"title": "Тихое место", "year": "2018", "rating": "7.5", "genre": "Ужасы / Фантастика", "country": "США", "duration": "90 мин", "description": "Семья выживает в мире, где нельзя шуметь — монстры убивают за звук.", "player_url": "https://rutube.ru/video/search/тихое+место+1", "source": "RuTube"},
    {"title": "Пила: Игра на выживание", "year": "2004", "rating": "7.6", "genre": "Ужасы / Триллер", "country": "США", "duration": "103 мин", "description": "Два человека просыпаются в ловушке маньяка Конструктора.", "player_url": "https://rutube.ru/video/search/пила+1", "source": "RuTube"},
    {"title": "Пункт назначения", "year": "2000", "rating": "6.7", "genre": "Ужасы / Триллер", "country": "США", "duration": "98 мин", "description": "Подросток предвидит авиакатастрофу и спасает друзей.", "player_url": "https://rutube.ru/video/search/пункт+назначения+1", "source": "RuTube"},
    {"title": "Техасская резня бензопилой", "year": "2003", "rating": "6.2", "genre": "Ужасы", "country": "США", "duration": "98 мин", "description": "Подростки встречают семью каннибалов в Техасе.", "player_url": "https://rutube.ru/video/search/техасская+резня+бензопилой+2003", "source": "RuTube"},
    {"title": "Кошмар на улице Вязов", "year": "1984", "rating": "7.4", "genre": "Ужасы", "country": "США", "duration": "91 мин", "description": "Фредди Крюгер убивает подростков во сне.", "player_url": "https://rutube.ru/video/search/кошмар+на+улице+вязов+1", "source": "RuTube"},
    {"title": "Пятница 13-е", "year": "1980", "rating": "6.4", "genre": "Ужасы", "country": "США", "duration": "95 мин", "description": "Вожатые в летнем лагере погибают от руки убийцы.", "player_url": "https://rutube.ru/video/search/пятница+13+1", "source": "RuTube"},
    {"title": "Хэллоуин", "year": "1978", "rating": "7.7", "genre": "Ужасы", "country": "США", "duration": "91 мин", "description": "Майкл Майерс возвращается в родной город для убийств.", "player_url": "https://rutube.ru/video/search/хэллоуин+1978", "source": "RuTube"},
    {"title": "Крик", "year": "1996", "rating": "7.4", "genre": "Ужасы / Триллер", "country": "США", "duration": "111 мин", "description": "Маньяк в маске убивает подростков в маленьком городке.", "player_url": "https://rutube.ru/video/search/крик+1", "source": "RuTube"},
    {"title": "Звонок", "year": "2002", "rating": "7.1", "genre": "Ужасы", "country": "США", "duration": "115 мин", "description": "Журналистка расследует тайну видеокассеты, убивающей через 7 дней.", "player_url": "https://rutube.ru/video/search/звонок+2002", "source": "RuTube"},
    {"title": "Ведьма из Блэр", "year": "1999", "rating": "6.5", "genre": "Ужасы", "country": "США", "duration": "81 мин", "description": "Студенты снимают документалку о ведьме и пропадают в лесу.", "player_url": "https://rutube.ru/video/search/ведьма+из+блэр", "source": "RuTube"},
    {"title": "Паранормальное явление", "year": "2007", "rating": "6.3", "genre": "Ужасы", "country": "США", "duration": "86 мин", "description": "Пара снимает на камеру странные события в доме.", "player_url": "https://rutube.ru/video/search/паранормальное+явление+1", "source": "RuTube"},
    {"title": "Астрал", "year": "2010", "rating": "6.8", "genre": "Ужасы", "country": "США", "duration": "103 мин", "description": "Семья спасает сына из астрального мира.", "player_url": "https://rutube.ru/video/search/астрал+1", "source": "RuTube"},
    {"title": "Ван Хельсинг", "year": "2004", "rating": "6.1", "genre": "Боевик / Фэнтези", "country": "США", "duration": "132 мин", "description": "Охотник на монстров сражается с Дракулой в Трансильвании.", "player_url": "https://rutube.ru/video/search/ван+хельсинг", "source": "RuTube"},
    {"title": "Константин: Повелитель тьмы", "year": "2005", "rating": "7.0", "genre": "Фэнтези / Боевик", "country": "США", "duration": "121 мин", "description": "Экзорцист сражается с демонами и дьяволом.", "player_url": "https://rutube.ru/video/search/константин", "source": "RuTube"},
    {"title": "Доктор Стрэндж", "year": "2016", "rating": "7.5", "genre": "Фэнтези / Боевик", "country": "США", "duration": "115 мин", "description": "Хирург становится мастером мистических искусств.", "player_url": "https://rutube.ru/video/search/доктор+стрэндж+1", "source": "RuTube"},
    {"title": "Чёрная пантера", "year": "2018", "rating": "7.3", "genre": "Фэнтези / Боевик", "country": "США", "duration": "134 мин", "description": "Т'Чалла становится королём Ваканды и Чёрной пантерой.", "player_url": "https://rutube.ru/video/search/чёрная+пантера", "source": "RuTube"},
    {"title": "Капитан Марвел", "year": "2019", "rating": "6.8", "genre": "Боевик / Фантастика", "country": "США", "duration": "123 мин", "description": "Кэрол Дэнверс обретает силы и вспоминает прошлое.", "player_url": "https://rutube.ru/video/search/капитан+марвел", "source": "RuTube"},
    {"title": "Человек-муравей", "year": "2015", "rating": "7.3", "genre": "Боевик / Фантастика", "country": "США", "duration": "117 мин", "description": "Вор получает костюм, уменьшающий до размера муравья.", "player_url": "https://rutube.ru/video/search/человек+муравей+1", "source": "RuTube"},
    {"title": "Веном", "year": "2018", "rating": "6.7", "genre": "Фантастика / Боевик", "country": "США", "duration": "112 мин", "description": "Журналист становится носителем инопланетного симбиота.", "player_url": "https://rutube.ru/video/search/веном+1", "source": "RuTube"},
    {"title": "Новый Человек-паук", "year": "2012", "rating": "6.9", "genre": "Боевик / Фантастика", "country": "США", "duration": "136 мин", "description": "Питер Паркер ищет убийцу дяди и сражается с Ящером.", "player_url": "https://rutube.ru/video/search/новый+человек+паук+1", "source": "RuTube"},
    {"title": "Человек-паук: Возвращение домой", "year": "2017", "rating": "7.4", "genre": "Боевик / Фантастика", "country": "США", "duration": "133 мин", "description": "Питер учится в школе и сражается со Стервятником.", "player_url": "https://rutube.ru/video/search/человек+паук+возвращение+домой", "source": "RuTube"},
    {"title": "Человек-паук: Вдали от дома", "year": "2019", "rating": "7.4", "genre": "Боевик / Фантастика", "country": "США", "duration": "129 мин", "description": "Питер едет в Европу и сражается с Мистерио.", "player_url": "https://rutube.ru/video/search/человек+паук+вдали+от+дома", "source": "RuTube"},
    {"title": "Человек-паук: Нет пути домой", "year": "2021", "rating": "8.2", "genre": "Боевик / Фантастика", "country": "США", "duration": "148 мин", "description": "Питер открывает мультивселенную и встречает старых врагов.", "player_url": "https://rutube.ru/video/search/человек+паук+нет+пути+домой", "source": "RuTube"},
    {"title": "Бэтмен", "year": "2022", "rating": "7.8", "genre": "Боевик / Драма", "country": "США", "duration": "176 мин", "description": "Брюс Уэйн охотится на Загадочника в Готэме.", "player_url": "https://rutube.ru/video/search/бэтмен+2022", "source": "RuTube"},
    {"title": "Лига справедливости Зака Снайдера", "year": "2021", "rating": "7.9", "genre": "Боевик / Фантастика", "country": "США", "duration": "242 мин", "description": "Расширенная версия Лиги справедливости от Зака Снайдера.", "player_url": "https://rutube.ru/video/search/лига+справедливости+снайдер", "source": "RuTube"},
    {"title": "Шазам!", "year": "2019", "rating": "7.0", "genre": "Фэнтези / Боевик", "country": "США", "duration": "132 мин", "description": "Подросток превращается в супергероя по волшебству.", "player_url": "https://rutube.ru/video/search/шазам", "source": "RuTube"},
    {"title": "Чёрный Адам", "year": "2022", "rating": "6.2", "genre": "Фэнтези / Боевик", "country": "США", "duration": "125 мин", "description": "Древний суперзлодей пробуждается в современном мире.", "player_url": "https://rutube.ru/video/search/чёрный+адам", "source": "RuTube"},
    {"title": "Флэш", "year": "2023", "rating": "6.7", "genre": "Фантастика / Боевик", "country": "США", "duration": "144 мин", "description": "Барри Аллен путешествует во времени и меняет реальность.", "player_url": "https://rutube.ru/video/search/флэш+2023", "source": "RuTube"},
    {"title": "Синий Жук", "year": "2023", "rating": "5.9", "genre": "Фантастика / Боевик", "country": "США", "duration": "127 мин", "description": "Парень получает инопланетный костюм-жук.", "player_url": "https://rutube.ru/video/search/синий+жук", "source": "RuTube"},
    {"title": "Элвис", "year": "2022", "rating": "7.3", "genre": "Драма / Биография", "country": "США", "duration": "159 мин", "description": "История жизни короля рок-н-ролла Элвиса Пресли.", "player_url": "https://rutube.ru/video/search/элвис+2022", "source": "RuTube"},
    {"title": "Богемская рапсодия", "year": "2018", "rating": "7.9", "genre": "Драма / Биография", "country": "США", "duration": "134 мин", "description": "История Фредди Меркьюри и группы Queen.", "player_url": "https://rutube.ru/video/search/богемская+рапсодия", "source": "RuTube"},
    {"title": "Рокетмен", "year": "2019", "rating": "7.3", "genre": "Драма / Биография", "country": "Великобритания", "duration": "121 мин", "description": "История жизни Элтона Джона.", "player_url": "https://rutube.ru/video/search/рокетмен", "source": "RuTube"},
    {"title": "Дюна: Часть вторая", "year": "2024", "rating": "8.5", "genre": "Фантастика / Приключения", "country": "США", "duration": "166 мин", "description": "Пол Атрейдес объединяется с фрименами против Харконненов.", "player_url": "https://rutube.ru/video/search/дюна+2", "source": "RuTube"},
    {"title": "Оппенгеймер", "year": "2023", "rating": "8.3", "genre": "Драма / Биография", "country": "США", "duration": "180 мин", "description": "История создания атомной бомбы Робертом Оппенгеймером.", "player_url": "https://rutube.ru/video/search/оппенгеймер", "source": "RuTube"},
    {"title": "Барби", "year": "2023", "rating": "6.8", "genre": "Комедия / Фэнтези", "country": "США", "duration": "114 мин", "description": "Барби попадает в реальный мир и ищет смысл существования.", "player_url": "https://rutube.ru/video/search/барби+2023", "source": "RuTube"},
    {"title": "Ёж Соник", "year": "2020", "rating": "6.5", "genre": "Фантастика / Комедия", "country": "США", "duration": "99 мин", "description": "Синий ёж с суперскоростью дружит с человеком.", "player_url": "https://rutube.ru/video/search/ёж+соник+1", "source": "RuTube"},
    {"title": "Ёж Соник 2", "year": "2022", "rating": "6.5", "genre": "Фантастика / Комедия", "country": "США", "duration": "122 мин", "description": "Соник и Наклз сражаются с доктором Роботником.", "player_url": "https://rutube.ru/video/search/ёж+соник+2", "source": "RuTube"},
    {"title": "Невероятная жизнь Уолтера Митти", "year": "2013", "rating": "7.3", "genre": "Драма / Приключения", "country": "США", "duration": "114 мин", "description": "Офисный работник отправляется в реальное приключение.", "player_url": "https://rutube.ru/video/search/уолтер+митти", "source": "RuTube"},
    {"title": "Стажёр", "year": "2015", "rating": "7.1", "genre": "Комедия / Драма", "country": "США", "duration": "121 мин", "description": "70-летний вдовец становится стажёром в модном стартапе.", "player_url": "https://rutube.ru/video/search/стажёр", "source": "RuTube"}
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
            f"📚 <b>{len(MOVIES_DB)}</b> фильмов бесплатно!\n"
            f"✅ Без подписки — смотри бесплатно!\n\n"
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
    await message.answer(text, parse_mode="HTML", reply_markup=get_movie_kb(m['player_url']))

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
            await message.answer(text, parse_mode="HTML", reply_markup=get_movie_kb(m['player_url']))
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔍 Найти на YouTube", url=f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}+смотреть+бесплатно")]])
        await message.answer(f"😔 <b>{message.text}</b> не найден в базе.\n\nПопробуйте YouTube:", parse_mode="HTML", reply_markup=kb)

async def main():
    logger.info("🚀 Запуск бота «Что посмотреть?»...")
    logger.info(f"📊 Фильмов в базе: {len(MOVIES_DB)}")
    logger.info(f"💾 Источники: RuTube, YouTube")
    logger.info(f"Токен: {BOT_TOKEN[:20]}...")
    
    # Проверка базы
    for i, movie in enumerate(MOVIES_DB):
        if 'title' not in movie or 'player_url' not in movie:
            logger.error(f"Фильм {i} не имеет title или player_url!")
    
    logger.info("✅ База проверена")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
