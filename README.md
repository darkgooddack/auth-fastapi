##  📌 Описание репозитория auth-fastapi
### 🔹 О проекте
**auth-fastapi** — это простой и безопасный сервис аутентификации и авторизации, реализованный с использованием FastAPI, PostgreSQL и SQLAlchemy. Проект включает регистрацию пользователей, аутентификацию через JWT-токены и защиту маршрутов.

### 🚀 Функционал
##### ✅ Регистрация пользователей
##### ✅ Аутентификация по JWT
##### ✅ Хеширование паролей (bcrypt)
##### ✅ Подключение к PostgreSQL через SQLAlchemy
##### ✅ Разделение логики по модулям
##### ✅ Миграции базы данных с Alembic

### 📂 Структура проекта
```
/app
│── /core         # Конфигурация, безопасность
│── /models       # SQLAlchemy-модели
│── /schemas      # Pydantic-схемы
│── /crud         # CRUD-операции
│── /routers      # Роутеры FastAPI
│── main.py       # Точка входа
```
### 🔧 Установка и запуск
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
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
### 🔑 Использование API
##### 🔹 Регистрация
POST /users/register
```
{
    "username": "testuser",
    "password": "password123"
}
```
##### 🔹 Авторизация
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

##### 🔹 Доступ к защищённому ресурсу

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
### 📌 TODO
##### 🔹 Подключение Redis для хранения токенов ✅
##### 🔹 Добавление refresh-токенов
##### 🔹 Логирование и мониторинг ✅
