# Сервис для сбора перформанс метрик сервисов

## Настройка окружения
```commandline
poetry install
poetry shell
```
## Запуск тестов
```commandline
pytest --cov
```

## Запуск dev окружения
Сначала поднять сервис с помощью docker compose (запустится постгрес и наш сервис)
```commandline
docker compose up --build -d
```
Прогнать миграции
```commandline
alembic migrate head
```
Доступ к сервису осуществляется по адресу `http://localhost:8080`
Swagger доступен по адресу `http://localhost:8080/docs`
