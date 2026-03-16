# electronics_network_platform

Веб-приложение для управления сетью продаж электроники.  
Проект выполнен как тестовое задание на Django + Django REST Framework + PostgreSQL.

## Цель проекта

Реализовать backend-систему для управления иерархической сетью по продаже электроники, включающую:

- API на Django REST Framework
- admin-панель Django
- PostgreSQL
- модель сети из звеньев разных уровней
- продукты, связанные со звеньями сети
- ограничения бизнес-логики
- фильтрацию и права доступа по требованиям ТЗ

## Бизнес-логика

Сеть продаж состоит из 3 уровней:

- завод
- розничная сеть
- индивидуальный предприниматель

Каждое звено сети:

- имеет название
- имеет тип звена
- хранит контактные данные
- хранит поставщика
- хранит задолженность перед поставщиком
- содержит связанные продукты

## Технологический стек

### Backend

- Python 3.13.7
- Django 6.0.3
- Django REST Framework
- PostgreSQL
- django-filter
- drf-spectacular
- python-dotenv
- psycopg 3 (`psycopg[binary]`)

### Dev tools

- pytest
- pytest-django
- black
- isort
- flake8

## Что реализовано

### Модели

#### NetworkNode

Поля:

- `name`
- `node_type`
- `email`
- `country`
- `city`
- `street`
- `house_number`
- `supplier`
- `debt`
- `created_at`

#### Product

Поля:

- `network_node`
- `name`
- `model`
- `release_date`

### Реализованные ограничения бизнес-логики

- объект не может ссылаться сам на себя как на поставщика
- завод не может иметь поставщика
- не-завод должен иметь поставщика
- запрещены циклические связи
- глубина иерархии ограничена 3 уровнями
- через API нельзя изменять поле `debt`

### Admin panel

Реализовано:

- отображение звеньев сети
- отображение продуктов
- inline-редактирование продуктов в карточке звена
- ссылка на поставщика
- фильтрация по городу
- фильтрация по стране
- фильтрация по типу звена
- action для очистки задолженности

### API

Реализован CRUD для:

- `NetworkNode`
- `Product`

Для `NetworkNode` используются отдельные сериализаторы для:

- списка
- деталей
- создания
- обновления

### Фильтрация

Для `NetworkNode` реализована фильтрация по стране:

`GET /api/nodes/?country=South Korea`

Фильтрация работает без учёта регистра.

### Права доступа

Доступ к API разрешён только пользователям, которые одновременно:

- аутентифицированы
- активны (`is_active=True`)
- являются сотрудниками (`is_staff=True`)

## Структура проекта

```text
electronics_network_platform/
├─ config/
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ network/
│  ├─ migrations/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ filters.py
│  ├─ models.py
│  ├─ permissions.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ .env
├─ .env.example
├─ .gitignore
├─ manage.py
├─ README.md
└─ requirements.txt
```

## Установка и запуск проекта

### 1. Клонировать репозиторий

```bash
git clone <repo_url>
cd electronics_network_platform
```

### 2. Создать и активировать виртуальное окружение

#### Windows PowerShell

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Создать `.env`

Скопировать `.env.example` в `.env` и заполнить переменные окружения.

Пример:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=electronics_network_platform
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

Используй актуальные имена переменных из файла `.env.example` и `settings.py`.

### 5. Применить миграции

```bash
python manage.py migrate
```

### 6. Создать суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запустить сервер

```bash
python manage.py runserver
```

После запуска проект будет доступен по адресу:

`http://127.0.0.1:8000/`

## Основные URL

### Admin panel

`http://127.0.0.1:8000/admin/`

### OpenAPI schema

`http://127.0.0.1:8000/api/schema/`

### Swagger UI

`http://127.0.0.1:8000/api/docs/`

### ReDoc

`http://127.0.0.1:8000/api/redoc/`

## Примеры API endpoints

### Звенья сети

- `GET /api/nodes/` — список звеньев сети
- `POST /api/nodes/` — создание звена сети
- `GET /api/nodes/{id}/` — детали звена
- `PATCH /api/nodes/{id}/` — частичное обновление
- `DELETE /api/nodes/{id}/` — удаление

### Продукты

- `GET /api/products/` — список продуктов
- `POST /api/products/` — создание продукта
- `GET /api/products/{id}/` — детали продукта
- `PATCH /api/products/{id}/` — частичное обновление
- `DELETE /api/products/{id}/` — удаление

## Пример фильтрации

Получить только звенья из South Korea:

`GET /api/nodes/?country=South Korea`

## Проверенные требования ТЗ

Реализовано:

- Django-проект с PostgreSQL
- admin-панель
- API на DRF
- модель сети продаж электроники
- self-FK на поставщика
- ограничение глубины иерархии
- защита от циклов
- продукты, связанные со звеньями
- запрет обновления `debt` через API
- фильтрация по стране
- доступ к API только для active staff пользователей
