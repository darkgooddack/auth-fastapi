import logging
import redis
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.crud.user import get_user_by_username
from app.schemas.user import UserCreate
from fastapi.security import OAuth2PasswordBearer
import jwt
from redis.exceptions import RedisError
from datetime import timedelta
from app.core.config import settings

# Settings
SECRET_KEY = "your_secret_key"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Connecting to Redis
try:
     redis_client = redis.Redis(
        host=settings.REDIS_HOST,       # теперь берётся из .env или настроек
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )
    redis_client.ping()
    logging.info("✅ Connected to Redis")
except RedisError:
    logging.critical("🚨 Connection error to Redis! Make sure the Redis server is running.")
    redis_client = None  # Disable Redis so that the code can work without it

router = APIRouter()
logging.basicConfig(level=logging.INFO)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", summary="User authentication")
async def login(user: UserCreate, db: Session = Depends(get_db)):
    """
   **User authentication**
    - 🔑 Verifies login and password.
    - 🎫 Returns a JWT token for accessing protected APIs.
    - ❌ Error if the login or password is incorrect.
    """
    logging.info(f"✅ Authentication request for user: {user.username}")

    db_user = get_user_by_username(db, user.username)

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        logging.error("❌ Error: Invalid credentials!")
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Generate token with expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)

    # Save token in Redis if available
    if redis_client:
        try:
            redis_client.setex(f"token:{db_user.username}", ACCESS_TOKEN_EXPIRE_MINUTES * 60, access_token)
            logging.info(f"✅ Token for user {db_user.username} saved in Redis")
        except RedisError:
            logging.error("⚠️ Error while saving token in Redis")

    logging.info(f"✅ Token issued to user: {db_user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    """
    **Protected route**
    - Checks token in Redis.
    - Returns a message if the token is valid.
    """
    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")

        # Verify token in Redis (if Redis is available)
        if redis_client:
            stored_token = redis_client.get(f"token:{user_id}")
            if stored_token is None:
                logging.error(f"❌ Token not found in Redis for user {user_id}")
                raise HTTPException(status_code=401, detail="Invalid token")

            if stored_token != token:
                logging.error(f"❌ Token for user {user_id} does not match the one stored in Redis")
                raise HTTPException(status_code=401, detail="Invalid token")

        logging.info(f"✅ Access granted for user {user_id}")
        return {"message": f"Hello, {user_id}! Your token is valid."}

    except jwt.PyJWTError:
        logging.error("❌ Error: Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """
    **Logout**
    - Deletes the token from Redis.
    - The user is logged out.
    """
    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")

        if redis_client:
            try:
                if redis_client.delete(f"token:{user_id}"):
                    logging.info(f"✅ User {user_id} logged out, token deleted from Redis")
                    return {"message": "You have successfully logged out"}
                else:
                    logging.warning(f"⚠️ Logout attempt: Token for user {user_id} is already missing in Redis")
                    return {"message": "Token is already invalid or missing"}
            except RedisError:
                logging.error("⚠️ Error while deleting token from Redis")

        return {"message": "You have logged out, but Redis is unavailable"}

    except jwt.ExpiredSignatureError:
        logging.warning("⚠️ Logout attempt with an already expired token")
        return {"message": "You have already logged out (token expired)"}
