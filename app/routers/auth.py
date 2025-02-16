from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, crud, auth
from app.database import get_db

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/auth", response_model=schemas.AuthResponse)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, form_data.username)
    if not user:
        user = crud.create_user(db, schemas.AuthRequest(
            username=form_data.username,
            password=form_data.password
        ))
    elif not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = auth.create_access_token(
        data={"sub": user.username}
    )
    return {"token": access_token}