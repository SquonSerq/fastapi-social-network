from typing import Any, Optional

import models
import schemas
from core.security import get_password_hash, verify_password
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDPost(CRUDBase[models.Post, schemas.PostCreate, schemas.PostUpdate]):
	def create(self, db: Session, *, post_in: schemas.PostCreate, user: models.User):
		db_obj = models.Post(title=post_in.title, post_text=post_in.post_text, creator_id=user.id)
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj
	
	def get_by_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100):
		db_obj = db.query(models.Post).filter(models.Post.creator_id == user_id).offset(skip).limit(limit).all()
		return db_obj

	def get_likes(self, db: Session, *, post_id: int):
		db_obj = db.query(models.Like).filter(models.Like.post_id == post_id).all()
		return db_obj

	def get_dislikes(self, db: Session, *, post_id: int):
		db_obj = db.query(models.Dislike).filter(models.Dislike.post_id == post_id).all()
		return db_obj

post = CRUDPost(models.Post)