from pydantic import BaseModel

class DislikeBase(BaseModel):
	user_id: int
	post_id: int

class DislikeInDBBase(DislikeBase):
	id: int

	class Config:
		orm_mode = True

class Dislike(DislikeInDBBase):
	pass

class DislikeInDB(DislikeInDBBase):
	pass

class DislikeUpdate(DislikeBase):
	pass

class DislikeCreate(DislikeBase):
	pass
