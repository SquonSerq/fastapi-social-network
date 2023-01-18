from pydantic import BaseModel

class LikeBase(BaseModel):
	user_id: int
	post_id: int

class LikeInDBBase(LikeBase):
	id: int

	class Config:
		orm_mode = True

class Like(LikeInDBBase):
	pass

class LikeInDB(LikeInDBBase):
	pass

class LikeUpdate(LikeBase):
	pass

class LikeCreate(LikeBase):
	pass
