# 🎬 Telegram Bot "Что посмотреть?"

Telegram бот для поиска и просмотра фильмов со встроенным видеоплеером.

## ✨ Возможности

- 🎥 **Парсинг фильмов** с Кинопоиска и IMDb (топ-250)
- 📺 **Встроенный видеоплеер** через Telegram WebApp
- 🔍 **Поиск фильмов** по названию
- 🎬 **Быстрый доступ** к популярным фильмам
- 📱 **Адаптивный дизайн** для мобильных устройств

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Получение токена бота

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен

### 3. Настройка

Откройте `bot.py` и замените токен:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Вставьте ваш токен
```

### 4. Запуск бота

```bash
python bot.py
```

## 📋 Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие и инструкция |
| `/movies` | Показать подборку фильмов |
| `/search` | Поиск фильма по названию |

## 🎮 Как использовать WebApp плеер

1. Нажмите кнопку **"🎬 Смотреть онлайн"** под фильмом
2. Откроется встроенный плеер внутри Telegram
3. Выберите фильм из популярных или введите название для поиска
4. Смотрите фильм!

## 📁 Структура проекта

```
telegram-movie-bot/
├── bot.py              # Основной код бота
├── webapp.html         # WebApp для видеоплеера
├── requirements.txt    # Зависимости Python
├── README.md          # Документация
└── .gitignore         # Git ignore файл
```

## 🔧 Настройка WebApp

Для работы WebApp необходимо:

1. Разместить `webapp.html` на любом хостинге (GitHub Pages, Vercel, Netlify)
2. В @BotFather настроить WebApp URL для вашего бота:
   - Отправьте `/mybot`
   - Выберите своего бота
   - Нажмите "Menu Button" → "Configure Menu Button"
   - Отправьте ссылку на ваш `webapp.html`

## 🛠 Технологии

- **Python 3.8+**
- **aiogram 3.x** - асинхронный фреймворк для Telegram Bot API
- **aiohttp** - асинхронный HTTP-клиент
- **BeautifulSoup4** - парсинг HTML
- **Telegram WebApp** - встроенные веб-приложения

## 📝 Примечания

> ⚠️ **Важно**: Бот использует YouTube для поиска фильмов. Для просмотра полного доступа к контенту убедитесь в соблюдении авторских прав.

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте ветку (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 👤 Автор

Пет-проект для демонстрации возможностей Telegram Bot API + WebApp

## 🙏 Благодарности

- [aiogram documentation](https://docs.aiogram.dev/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram WebApp](https://core.telegram.org/bots/webapps)

---

⭐ **Если вам понравился проект, поставьте звезду на GitHub!**
