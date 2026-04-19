from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import models, schemas, auth


router = APIRouter()


# database dependency
def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# ---------------- REGISTER ----------------

@router.post("/register")

def register_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db)
):

    # check user exists
    existing_user = db.query(
        models.User
    ).filter(
        models.User.username == user.username
    ).first()


    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    # hash password
    hashed_password = auth.hash_password(
        user.password
    )


    new_user = models.User(

        username=user.username,

        password=hashed_password
    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return {

        "message": "User registered successfully"
    }


# ---------------- LOGIN ----------------

@router.post("/login")

def login_user(

        user: schemas.UserLogin,

        db: Session = Depends(get_db)
):

    db_user = db.query(
        models.User
    ).filter(
        models.User.username == user.username
    ).first()


    if not db_user:

        raise HTTPException(
            status_code=400,
            detail="Invalid username"
        )


    if not auth.verify_password(

            user.password,
            db_user.password
    ):

        raise HTTPException(

            status_code=400,

            detail="Invalid password"
        )


    # create token
    token = auth.create_access_token(

        {"user_id": db_user.id}

    )


    return {

        "access_token": token,

        "token_type": "bearer"
    }