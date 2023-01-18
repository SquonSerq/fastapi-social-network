import crud
import models
import schemas
from crud.base import CRUDBase
from sqlalchemy.orm import Session


class CRUDLike(CRUDBase[models.Like, schemas.LikeCreate, schemas.LikeUpdate]):
	def get(self, db: Session, *, post_id: int, user_id: int):
		db_obj = db.query(models.Like)\
			.filter(models.Like.post_id == post_id)\
			.filter(models.Like.user_id == user_id).first()	
		return db_obj

like = CRUDLike(models.Like)

class CRUDDislike(CRUDBase[models.Dislike, schemas.DislikeCreate, schemas.DislikeUpdate]):
	def get(self, db: Session, *, post_id: int, user_id: int):
		db_obj = db.query(models.Dislike)\
			.filter(models.Dislike.post_id == post_id)\
			.filter(models.Dislike.user_id == user_id).first()	
		return db_obj

dislike = CRUDDislike(models.Dislike)