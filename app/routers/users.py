import logging
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.crud.user import create_user, get_user_by_username
from app.schemas.user import UserCreate, UserOut

router = APIRouter()
logging.basicConfig(level=logging.INFO)

@router.post(
    "/register",
    response_model=UserOut,
    summary="Register a new user",
    description="""
    Creates a new user in the system.  
    If a user with the same username already exists, returns an error.  
    The password will be encrypted before storage.
    """,
    responses={
        201: {"description": "User successfully registered"},
        400: {"description": "User already exists"}
    },
)
async def register(
        username: str = Form(..., description="Username"),
        password: str = Form(..., description="Password"),
        db: Session = Depends(get_db)
):
    """
    **User Registration**
    - 🔑 Creates a new user.
    - ❌ Returns an error if the user is already registered.
    - 🔒 The password is stored in an encrypted format.
    """

    logging.info(f"✅ Attempting to register user: {username}")

    if get_user_by_username(db, username):
        logging.warning(f"❌ Registration failed: user {username} already exists")
        raise HTTPException(status_code=400, detail="User already exists")

    # 🔥 Create a UserCreate object before passing it to create_user
    user_data = UserCreate(username=username, password=password)
    new_user = create_user(db, user_data)
    logging.info(f"✅ User {username} successfully registered")

    return new_user
