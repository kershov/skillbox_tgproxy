# Flask-Proxy для работы с Telegram API

Простое приложение, выступащее в роли прокси для работы с Telegram API. Разработано в качестве дополнения к дипломной работе, выполняемой в рамках курса "Java-разработчик с нуля" от Skillbox.

**Стек:**

- Python 3.6
- Flask + SSLfy + Requests + PyJWT
- Heroku (https://heroku.com)


## Генерация JSON Web Token

Сгенерировать можно по ссылке: https://jwt.io/ или с помощью приложения, выполнив команду:

```bash
$ . venv/Scripts/activate
$ flask jwtgen --help
$ flask jwtgen --token-id BlogApp --secret "This is a secret" --exp=100
```

**Пример результата:**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODI3NTA2MjUsImV4cCI6MTU5MTM5MDYyNSwiaWQiOiJCbG9nQXBwIn0.e30vpV-UcFfiFDKm6IhTOX0eXLy19n40VOznwsKZQos"
}
```

**Формат токена:**

```json
{
  "iat": 1234567,
  "exp": 1239999,
  "id": "token_id"
}
```

## Деплой на Heroku

Убедиться, что переменные окружения (`AUTHORIZED_APP`, `JWT_SECRET_KEY`, `TELEGRAM_CHAT_ID`, `TELEGRAM_TOKEN`, `WEB_CONCURRENCY`) установлены:

```bash
$ heroku config
```

Установить необходимые переменные окружения, если не установлены:

```bash
heroku config:set AUTHORIZED_APP=BlogApp
heroku config:set JWT_SECRET_KEY=***
heroku config:set TELEGRAM_CHAT_ID=-100***
heroku config:set TELEGRAM_TOKEN=***:******
heroku config:set WEB_CONCURRENCY=3
```

## Деплой после изменений

```bash
$ git add .
$ git commit -m "Changes..."
$ git push heroku master
```

## Запуск локального сервера под Windows

```bash
$ . venv/Scripts/activate
$ heroku local -f Procfile.windows web
```
