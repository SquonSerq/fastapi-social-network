import crud
from core.security import ALGORITHM, SECRET_KEY
from db.database import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from schemas.login import TokenData
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(email=username)
    except JWTError:
        raise credentials_exception
    user = crud.user.get_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        credentials_exception["detail"] = "User is not active"
        raise credentials_exception
    return user