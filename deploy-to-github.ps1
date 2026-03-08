# Скрипт для загрузки проекта на GitHub
# Запустите в PowerShell из директории проекта

Write-Host "=== Загрузка Telegram Movie Bot на GitHub ===" -ForegroundColor Cyan

# Проверка наличия Git
try {
    $gitVersion = git --version 2>$null
    if ($null -eq $gitVersion) {
        throw "Git not found"
    }
    Write-Host "Git найден: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Git не установлен! Установите Git с https://git-scm.com/" -ForegroundColor Red
    Write-Host "`nИли используйте ручную загрузку через GitHub Desktop" -ForegroundColor Yellow
    exit 1
}

# Инициализация репозитория
Write-Host "`n[1/5] Инициализация Git репозитория..." -ForegroundColor Cyan
git init

# Добавление файлов
Write-Host "[2/5] Добавление файлов..." -ForegroundColor Cyan
git add .

# Первый коммит
Write-Host "[3/5] Создание коммита..." -ForegroundColor Cyan
git commit -m "Initial commit: Telegram Movie Bot with WebApp player"

# Запрос данных репозитория
Write-Host "`n[4/5] Настройка удаленного репозитория" -ForegroundColor Cyan
$username = Read-Host "Введите ваше имя пользователя GitHub"
$repoName = Read-Host "Введите имя репозитория (или нажмите Enter для 'telegram-movie-bot')"

if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "telegram-movie-bot"
}

$remoteUrl = "https://github.com/$username/$repoName.git"
Write-Host "URL репозитория: $remoteUrl" -ForegroundColor Gray

# Проверка существования удаленного репозитория
$createRepo = Read-Host "Создать новый репозиторий на GitHub? (y/n)"

if ($createRepo -eq 'y' -or $createRepo -eq 'Y') {
    Write-Host "`nДля создания репозитория через CLI выполните:" -ForegroundColor Yellow
    Write-Host "gh repo create $repoName --public --source=. --remote=origin" -ForegroundColor Gray
    Write-Host "`nИли создайте репозиторий вручную на https://github.com/new" -ForegroundColor Yellow
}

git remote add origin $remoteUrl 2>$null
if ($LASTEXITCODE -ne 0) {
    git remote set-url origin $remoteUrl
}

# Push на GitHub
Write-Host "`n[5/5] Загрузка на GitHub..." -ForegroundColor Cyan
Write-Host "Введите ваши учетные данные GitHub при запросе" -ForegroundColor Yellow
git branch -M main
git push -u origin main

Write-Host "`n=== Загрузка завершена! ===" -ForegroundColor Green
Write-Host "Ваш репозиторий: https://github.com/$username/$repoName" -ForegroundColor Cyan

Write-Host "`n=== Следующие шаги ===" -ForegroundColor Cyan
Write-Host "1. Включите GitHub Pages для хостинга webapp.html"
Write-Host "2. Создайте бота в @BotFather и получите токен"
Write-Host "3. Настройте WebApp URL в @BotFather"
Write-Host "4. Запустите бота: python bot.py"
