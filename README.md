# Avito Shop

Микросервис для внутреннего использования сотрудниками Avito, позволяющий обмениваться виртуальными монетами и приобретать мерч. Сервис обеспечивает:

- Просмотр баланса и истории транзакций
- Покупку товаров из каталога мерча
- Безопасную передачу монет между пользователями
- JWT-аутентификацию

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=flat&logo=docker)](https://www.docker.com/)

---

## Технологии

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Alembic
- Pytest

---

## Запуск


### Инструкция
1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/SlavicSandwich/avito_internship.git
   cd avito_internship
2. Собрать и запустить при помощи docker-compose:
   ```bash
   docker-compose up --build
3. Применить миграции
   ```bash
   docker-compose exec app  alembic revision --autogenerate -m "Initial commit"
   ```

   ```bash
    docker-compose exec app alembic upgrade head
   ```

---

### Запуск тестов
Запуск тестов:
```
docker-compose exec app pytest tests/ -v
```

---

### Документация API
После запуска сервиса можно открыть документацию:
- SwaggerUI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc
