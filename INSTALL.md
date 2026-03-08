# 🚀 Инструкция по запуску Telegram бота "Что посмотреть?"

## Шаг 1: Установка Python

Если Python не установлен:
1. Скачайте с https://www.python.org/downloads/
2. При установке отметьте галочку "Add Python to PATH"

## Шаг 2: Установка зависимостей

Откройте PowerShell или Command Prompt в папке проекта и выполните:

```bash
pip install -r requirements.txt
```

## Шаг 3: Создание бота в Telegram

1. Откройте Telegram и найдите **@BotFather**
2. Отправьте команду `/newbot`
3. Введите имя бота (например: `Что посмотреть? Bot`)
4. Введите username бота (должен заканчиваться на `bot`, например: `movie_watch_bot`)
5. **Сохраните полученный токен** (выглядит как: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Шаг 4: Настройка бота

1. Откройте файл `bot.py`
2. Найдите строку: `BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"`
3. Замените `YOUR_BOT_TOKEN_HERE` на ваш токен из @BotFather

Пример:
```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

## Шаг 5: Загрузка на GitHub

### Вариант A: Автоматически (если установлен Git)

1. Установите Git: https://git-scm.com/download/win
2. Запустите PowerShell в папке проекта
3. Выполните:
   ```powershell
   .\deploy-to-github.ps1
   ```
4. Следуйте инструкциям

### Вариант B: Вручную через браузер

1. Зайдите на https://github.com
2. Нажмите **"New"** (зеленая кнопка)
3. Введите имя репозитория: `telegram-movie-bot`
4. Выберите **Public**
5. Нажмите **"Create repository"**
6. Вернитесь в папку проекта
7. Заархивируйте все файлы в ZIP
8. Перетащите ZIP в область upload на GitHub
   ИЛИ загрузите файлы по одному через **"uploading an existing file"**

## Шаг 6: Включение GitHub Pages (для WebApp)

1. В вашем репозитории на GitHub перейдите в **Settings**
2. В меню слева выберите **Pages**
3. В разделе "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **main** / **(root)**
4. Нажмите **Save**
5. Через 1-2 минуты ваш сайт будет доступен по:
   `https://ваш-username.github.io/telegram-movie-bot/webapp.html`

## Шаг 7: Настройка WebApp в BotFather

1. Откройте @BotFather
2. Отправьте `/mybot`
3. Выберите вашего бота
4. Нажмите **"Menu Button"**
5. Отправьте URL вашего WebApp:
   `https://ваш-username.github.io/telegram-movie-bot/webapp.html`
6. Введите название кнопки: `Смотреть фильмы`

## Шаг 8: Запуск бота

В PowerShell или Command Prompt выполните:

```bash
python bot.py
```

Вы должны увидеть:
```
2026-03-08 19:00:00 - INFO - Запуск бота...
2026-03-08 19:00:05 - INFO - Спарсено 10 фильмов
```

## Шаг 9: Проверка бота в Telegram

1. Откройте Telegram
2. Найдите вашего бота по username
3. Нажмите **Start** или отправьте `/start`
4. Попробуйте команду `/movies`

## 🎬 Готово!

Теперь вы можете:
- ✅ Получать подборки фильмов
- ✅ Смотреть фильмы через встроенный плеер
- ✅ Искать фильмы по названию

---

## 🔧 Возможные проблемы

### Ошибка "No module named 'aiogram'"
```bash
pip install aiogram aiohttp beautifulsoup4 lxml
```

### Git не найден
Установите Git: https://git-scm.com/download/win

### WebApp не открывается
Проверьте что GitHub Pages включен и URL доступен

### Бот не отвечает
Проверьте что токен введен правильно и бот запущен

## 📞 Поддержка

Если возникли вопросы, создайте Issue в репозитории GitHub.
