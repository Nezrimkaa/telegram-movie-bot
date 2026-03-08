# 📤 Загрузка на GitHub

## Быстрая загрузка (командная строка)

1. Создайте репозиторий на https://github.com/new
2. Имя: `telegram-movie-bot`
3. Не инициализируйте README (репозиторий уже создан)
4. Выполните команды:

```bash
cd C:\WINDOWS\system32\telegram-movie-bot

# Добавьте удаленный репозиторий (замените YOUR_USERNAME на ваш логин GitHub)
"C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/YOUR_USERNAME/telegram-movie-bot.git

# Переименуйте ветку
"C:\Program Files\Git\cmd\git.exe" branch -M main

# Загрузите на GitHub
"C:\Program Files\Git\cmd\git.exe" push -u origin main
```

## Альтернатива: GitHub Desktop

1. Скачайте https://desktop.github.com/
2. File → Add Local Repository → Выберите `C:\WINDOWS\system32\telegram-movie-bot`
3. Commit → Publish Repository

## После загрузки

1. Включите **GitHub Pages**: Settings → Pages → Branch: main → Save
2. Ваш WebApp будет доступен: `https://YOUR_USERNAME.github.io/telegram-movie-bot/webapp.html`
