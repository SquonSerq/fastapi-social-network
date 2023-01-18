import crud
import models
import schemas
from deps import get_current_user, get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	db_user = crud.user.get_by_email(db, email=user.email)
	if db_user:
		raise HTTPException(status_code=400, detail="Email already registered")
	return crud.user.create(db=db, obj_in=user)

@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
	users = crud.user.get_multi(db, skip=skip, limit=limit)
	return users