from datetime import timedelta
from typing import Any

import crud
import models
import schemas
from core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from deps import get_current_user, get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
	user = crud.user.authenticate(db=db, email=form_data.username, password=form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	# elif crud_user.is_active(user):
	# 	raise HTTPException(status_code=400, detail="Inactive user") 
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": user.email}, expires_delta=access_token_expires
	)
	return {"access_token": access_token, "token_type": "bearer"}

@router.post("/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(get_current_user)) -> Any:
    return current_user