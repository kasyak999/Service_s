Создание миграции

```
alembic revision --autogenerate -m "комментарий к миграции"
```

Создать докер
```
sudo docker compose -f docker-compose.debag.yml up --build
```
запустить
```
cd src
uvicorn app.main:app --reload
```