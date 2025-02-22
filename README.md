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
3️⃣ Настройка окружения
Создайте файл .env и укажите:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
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
uvicorn main:app --reload
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

##### 🔹 Доступ к защищённому ресурсу

GET /protected (с токеном)
```
Authorization: Bearer your_jwt_token
```
### 📌 TODO
##### 🔹 Подключение Redis для хранения токенов
##### 🔹 Добавление refresh-токенов
##### 🔹 Логирование и мониторинг
