### Проект Foodgram. Python-разработчик (бекенд) (Яндекс.Практикум)

![example workflow](https://github.com/Starkiller2000Turbo/foodgram-project-react/actions/workflows/main.yml/badge.svg)
[a link](https://food-project.hopto.org/)

### Описание:

Проект Foodgram - социальная сеть, в которой на основании Django ORM каждый пользователь может публиковать рецепты, а также редактировать или удалять свои уже существующие.

Была реализована система подписок на авторов рецептов на основании приложения django.contrib.auth.

К проекту были подключены базы данных SQL и POSTGRES, была реализована пагинация страниц, в админ-зоне обеспечено управление объектами.

С помощью docker реализована совместная работа frontend и backend.

Благодаря reportlab реализована возможность скачать список покупок в pdf, содержащий информацию о всех ингредиентах, необходимых для приготовления рецептов из списка покупок.

### Как установить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Starkiller2000Turbo/foodgram-project-react.git
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
cd backend
pip install -r requirements.txt
```

Для работы приложения необходим файл .env:

```
cd ..
touch .env
```

Необходимо заполнить файл .env следующим обазом:

```
SECRET_KEY=  
Секретный ключ для работы django.

DEBUG=
True/False в зависимости от необходимости режима отладки.

ALLOWED_HOSTS= 
Допустимые хосты, на которых будет работать приложение через пробел. 
Для локальной работы приложения - localhost и 127.0.0.1, для работы на сервере - также доменное имя и ip адрес. 

DATABASES= 
SQL в случае работы с файлом db.sqlite3, при работе с Postgres - любое другое значение. Другие базы данных не поддерживаются.

POSTGRES_DB= 
Название базы данных postgres.

POSTGRES_USER=
Имя пользователя базы данных postgres.

POSTGRES_PASSWORD=
Пароль пользователя базы данных postgres.

DB_HOST=
Адрес связи с базой данных.

DB_PORT=
Порт связи с базой данных.

```
### Как запустить backend:

Выполнить миграции для запуска backend:

```
make migrations
make migrate
```

Создать учетную запись администратора:

```
make superuser
```

Частично заполнить базу данных:

```
make tags
make ingredients
```

Если необходимо запустить исключительно backend, можно воспользоваться данной командой:

```
make run
```

### Как запустить весь проект локально:

Запустить проект локально:

```
cd infra
docker compose up
```

Ссылка на документацию проекта:

```
localhost/api/docs/
```

Выполнить миграции:

```
docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

Собрать статику:
```
docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```

Заполнить частично базу данных заранее собранными данными:
```
docker compose -f docker-compose.production.yml exec backend python manage.py import_tags
docker compose -f docker-compose.production.yml exec backend python manage.py import_ingredients
```

### Стек технологий использованный в проекте:

- Python
- Django
- Django REST Framework
- REST API
- SQLite
- Аутентификация по токену
- Reportlab
- Docker
- Workflow

### Автор:

- :white_check_mark: [Starkiller2000Turbo](https://github.com/Starkiller2000Turbo)