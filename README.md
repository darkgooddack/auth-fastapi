##  Repository Description: auth-fastapi
### About the Project
**auth-fastapi** is a secure and flexible authentication and authorization service built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. It supports user registration, JWT authentication, and route protection. Additionally, the project includes API endpoints for managing job listings from HH.ru.

### Features
##### ✅ User registration
##### ✅ JWT authentication
##### ✅ Token storage in Redis
##### ✅ CRUD operations for job listings from HH.ru
##### ✅ Password hashing (bcrypt)
##### ✅ PostgreSQL connection via SQLAlchemy
##### ✅ CORSMiddleware for integration with React

### Project Structure
```
/app
│── /core         # Configuration, security  
│── /models       # SQLAlchemy models  
│── /schemas      # Pydantic schemas  
│── /crud         # CRUD operations  
│── /routers      # FastAPI routers  
│── main.py       # Entry point  
```
### Installation and Setup
1️⃣ Clone the repository
```
git clone https://github.com/darkgooddack/auth-fastapi.git
cd auth-fastapi
```
2️⃣ Install dependencies
```
pip install -r requirements.txt
```
- psycopg2==2.9.10 for local debugging
- psycopg2-binary==2.9.10 for Docker 

3️⃣ Configure the environment
Create a .env file and specify:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
POSTGRES_PASSWORD=password
POSTGRES_PORT=5432

REDIS_HOST=redis <- заменить в своём .env
REDIS_PORT=6379
REDIS_DB=0

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
4️⃣ Start the database and migrations
```
alembic upgrade head
```
5️⃣ Start the server
```
docker run -d --name redis-container -p 6379:6379 redis
uvicorn main:app --reload
```
### API Usage

#### Added prefix: /api/v1

##### User Registration
POST /users/register
```
{
    "username": "testuser",
    "password": "password123"
}
```
##### Authentication
POST /auth/token
```
Content-Type: application/x-www-form-urlencoded

username=testuser&password=password123
```

✅ Response:
```
{
    "access_token": "your_jwt_token",
    "token_type": "bearer"
}
```
![img_3.png](img_3.png)
![img_4.png](img_4.png)

##### Accessing a Protected Resource

GET /protected (with token)
```
Authorization: Bearer your_jwt_token
```
![img.png](img.png)

##### Logout 

POST /logout (with token)
```
Authorization: Bearer your_jwt_token
```
![img_1.png](img_1.png)
![img_2.png](img_2.png)

### Job Listings API
#### 1. Create a Job Listing
##### POST /create

Creates a new job listing. If a listing with the same title already exists, an error is returned.

Parameters  (form-data):
- title (str) - Job title
- status (str) - Job status
- company_name (str) - Company name
- company_address (str) - Company address
- logo_url (str) - Company logo
- description (str) - Job description

Responses:
- 201 - Job successfully created
- 400 - Job already exists

#### 2. Update a Job Listing
##### PUT /update/{job_id}

Updates job information by ID.

Parameters (form-data):
- job_id (int) - Job ID
- title (str) - Job title
- status (str) - Job status
- company_name (str) - Company name
- company_address (str) - Company address
- logo_url (str) - Company logo
- description (str) - Job description

Responses:
- 200 - Job successfully updated
- 404 - Job not found

#### 3. Get a Job Listing by ID
##### GET /get/{job_id}

Returns job details by ID.

Parameters:
- job_id (int) - Job ID

Responses:
- 200 - Job found, returns job details
- 404 - Job not found

####  4. Удаление вакансии
###### DELETE /delete/{job_id}

Deletes a job listing by ID.

Parameters:
- job_id (int) - Job ID

Responses:
- 200 - Job successfully deleted
- 404 - Job not found

####  5. Parse Job Listings from HH.ru
###### POST /parse

This endpoint allows parsing job listings from HH.ru based on a given search query. It extracts job details and saves new job listings to the database if they don't already exist.

Query Parameters:
- search_query (string, required): Search query to filter job listings (e.g., "Python developer").
- count (integer, default: 10): Number of job listings to fetch (default is 10).

Example Request:

```
POST /parse?search_query=Python+developer&count=10
```

Response: If the request is successful, it returns a message with the number of added job listings.

Example Successful Response:
```
{
  "message": "Parsing completed",
  "added": 10
}
```
Errors:
- If the request to the HH.ru API fails (e.g., network issue or server downtime), a 500 error is returned.
- If the HH.ru API response is not valid JSON, a 500 error is also returned.
