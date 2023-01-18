from typing import Any, Optional

import models
import schemas
from core.security import get_password_hash, verify_password
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):
	def get_by_email(self, db: Session, *, email: str):
		return db.query(models.User).filter(models.User.email == email).first()

	def create(self, db: Session, *, obj_in: schemas.UserCreate) -> schemas.User:
		db_obj = models.User(
			email=obj_in.email,
			hashed_password=get_password_hash(obj_in.password),
		)
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj
	
	def update(
		self, db: Session, *, db_obj: models.User, obj_in: schemas.UserUpdate | dict[str, Any]
	) -> schemas.User:
		if isinstance(obj_in, dict):
			update_data = obj_in
		else:
			update_data = obj_in.dict(exclude_unset=True)
		if update_data["password"]:
			hashed_password = get_password_hash(update_data["password"])
			del update_data["password"]
			update_data["hashed_password"] = hashed_password
		return super().update(db, db_obj=db_obj, obj_in=update_data)

	def authenticate(self, db: Session, *, email: str, password: str) -> Optional[schemas.User]:
		user = self.get_by_email(db, email=email)
		if not user:
			return None
		if not verify_password(password, user.hashed_password):
			return None
		return user

	def is_active(self, user: schemas.User) -> bool:
		return user.is_active

user = CRUDUser(models.User)