# Learning Log

Django-проект для ведения личного журнала изучаемых тем и записей.

## Возможности

- регистрация, вход и POST-выход;
- личный список тем пользователя;
- создание тем;
- просмотр записей по теме;
- создание и редактирование записей;
- проверка владельца для тем и записей;
- оформление через `django-bootstrap4`.

## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Проверки

```bash
python manage.py check
python manage.py test
```

## Docker

```bash
cp .env.example .env
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

Production URL: `https://log.learning-logs.int.yt`
