# IT-Школа — лабораторная работа №2

Информационная система детской IT-школы (проект 3 курса): приём заявок на курсы, просмотр списка и карточки заявки, сценарии отказа.

## Запуск

### Docker Hub

```bash
docker pull ksushkaap/mispisit-lab1:0.0.2
docker run --rm -p 8080:8080 ksushkaap/mispisit-lab1:0.0.2
```

Откройте в браузере: http://localhost:8080

### Страницы

| Адрес | Назначение |
|-------|------------|
| `/` | Главная |
| `/requests` | Список заявок |
| `/requests/new` | Создание заявки |
| `/requests/1` | Карточка заявки |
| `/access-denied` | Отказ / ошибочный сценарий |

Пример отказа «чужая заявка»: http://localhost:8080/requests/1?parent_phone=%2B79999999999

## Локальная разработка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver 8080
```

## Данные

Справочник курсов: `core/data/courses.json` (только чтение).  
Заявки: `core/data/requests.json` (чтение и дополнение при отправке формы).

## Сборка и публикация образа 0.0.2

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ksushkaap/mispisit-lab1:0.0.2 --push .
```

Для GitVerse замените тег на `gitverse.ru/логин/mispisit-lab1:0.0.2` и выполните `docker login -u логин gitverse.ru` перед сборкой.

## Git

Создайте ветку `lab2`, отправьте изменения и откройте Pull Request в основную ветку — ссылку на PR приложите к отчёту.
