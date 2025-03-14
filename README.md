##  Описание репозитория auth-fastapi
### О проекте
**auth-fastapi** — это простой и безопасный сервис аутентификации и авторизации, реализованный с использованием FastAPI, PostgreSQL и SQLAlchemy. Проект включает регистрацию пользователей, аутентификацию через JWT-токены и защиту маршрутов.

### Функционал
##### ✅ Регистрация пользователей
##### ✅ Аутентификация по JWT
##### ✅ Хранение токенов в Redis
##### ✅ CRUD операции над вакансиями с hh.ru
##### ✅ Хеширование паролей (bcrypt)
##### ✅ Подключение к PostgreSQL через SQLAlchemy
##### ✅ CORSMiddleware для взаимодействия с React

### Структура проекта
```
/app
│── /core         # Конфигурация, безопасность
│── /models       # SQLAlchemy-модели
│── /schemas      # Pydantic-схемы
│── /crud         # CRUD-операции
│── /routers      # Роутеры FastAPI
│── main.py       # Точка входа
```
### Установка и запуск
1️⃣ Клонирование репозитория
```
git clone https://github.com/darkgooddack/auth-fastapi.git
cd auth-fastapi
```
2️⃣ Установка зависимостей
```
pip install -r requirements.txt
```
- psycopg2==2.9.10 для локальной отладки
- psycopg2-binary==2.9.10 для Docker 

3️⃣ Настройка окружения
Создайте файл .env и укажите:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
POSTGRES_PASSWORD=password
POSTGRES_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
4️⃣ Запуск базы данных и миграций
```
alembic upgrade head
```
5️⃣ Запуск сервера
```
docker run -d --name redis-container -p 6379:6379 redis
uvicorn main:app --reload
```
### Использование API

#### Был добавлен prefix=/api/v1

##### Регистрация
POST /users/register
```
{
    "username": "testuser",
    "password": "password123"
}
```
##### Авторизация
POST /auth/token
```
Content-Type: application/x-www-form-urlencoded

username=testuser&password=password123
```

✅ Ответ:
```
{
    "access_token": "your_jwt_token",
    "token_type": "bearer"
}
```
![img_3.png](img_3.png)
![img_4.png](img_4.png)

##### Доступ к защищённому ресурсу

GET /protected (с токеном)
```
Authorization: Bearer your_jwt_token
```
![img.png](img.png)

##### Logout 

POST /logout (с токеном)
```
Authorization: Bearer your_jwt_token
```
![img_1.png](img_1.png)
![img_2.png](img_2.png)

### API для вакансий
#### 1. Создание вакансии
##### POST /create

Создаёт новую вакансию. Если вакансия с таким названием уже существует, возвращает ошибку.

Параметры (form-data):
- title (str) - Название вакансии
- status (str) - Статус вакансии
- company_name (str) - Название компании
- company_address (str) - Адрес компании
- logo_url (str) - Логотип компании
- description (str) - Описание вакансии

Ответы
- 201 - Вакансия успешно создана
- 400 - Вакансия уже существует

#### 2. Обновление вакансии
##### PUT /update/{job_id}

Обновляет информацию о вакансии по ID.

Параметры (form-data):
- job_id (int) - ID вакансии
- title (str) - Название вакансии
- status (str) - Статус вакансии
- company_name (str) - Название компании
- company_address (str) - Адрес компании
- logo_url (str) - Логотип компании
- description (str) - Описание вакансии

Ответы
- 200 - Вакансия успешно обновлена
- 404 - Вакансия не найдена

#### 3. Получение вакансии по ID
##### GET /get/{job_id}

Возвращает информацию о вакансии по её ID.

Параметры:
- job_id (int) - ID вакансии

Ответы
- 200 - Вакансия найдена, возвращает объект вакансии
- 404 - Вакансия не найдена

####  4. Удаление вакансии
###### DELETE /delete/{job_id}

Удаляет вакансию по её ID.

Параметры:
- job_id (int) - ID вакансии

Ответы
- 200 - Вакансия успешно удалена
- 404 - Вакансия не найдена

####  5. Парсинг вакансий с hh.ru
###### Метод: POST /parse

Этот эндпоинт позволяет парсить вакансии с сайта hh.ru по заданному поисковому запросу. Он извлекает информацию о вакансиях и сохраняет новые вакансии в базу данных, если таких вакансий ещё нет.

Параметры запроса:
- search_query (строка, обязательный параметр): Поисковый запрос для фильтрации вакансий (например, "Python developer").
- count (целое число, по умолчанию 10): Количество вакансий для загрузки (по умолчанию — 10 вакансий).

Пример запроса:

```
POST /parse?search_query=Python+developer&count=10
```

Ответ: Если запрос прошёл успешно, возвращается сообщение с количеством добавленных вакансий.

Пример успешного ответа:
```
{
  "message": "Parsing completed",
  "added": 10
}
```
Ошибки:
- Если запрос к API hh.ru не удался (например, ошибка сети или сервер не ответил), возвращается ошибка с кодом 500.
- Если ответ от API hh.ru не является валидным JSON, также возвращается ошибка с кодом 500.
