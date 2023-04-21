![](frontend/public/favicon.png)

## проект foodgram
Социальная сеть основанная на рецептах и взаимодействии с ними.
Можно выкладывать свои рецепты, находить интересных авторов и подписываться на них.
Добовлять конкретные рецепты в изюронное, а так же в корзину покупок.

### установка на сервер 
* установите docker и docker-compose
* создайте файл .env 
#### пример заполнения env файла
```commandline
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
POSTGRES_USER=postgres 
POSTGRES_PASSWORD=password 
DB_HOST=db 
DB_PORT=5432 
SECRET_KEY=secretkey 
```
* запустите docker-compose ```docker-compose up -d --build```
* создаем миграции, суперпользователя, достаем статику
```commandline
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
```

### проект развернут
![example workflow](https://github.com/maxahist/foodgram-project-react/actions/workflows/main.yml/badge.svg)

http://84.201.139.213

### технолонии
* Python
* Docker
* React
* PostgreSQL

### автор проекта
https://github.com/maxahist