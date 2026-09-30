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

Запуск докера
```
sudo docker compose up --build 
```

Доступно по адресу
http://0.0.0.0:9000/admin/

.env
```
POSTGRES_USER=user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django
POSTGRES_PORT=5433
SECRET=SECRET4
DEBUG=false
```