from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from deps import get_db, get_current_user
from sqlalchemy.orm import Session

import crud, models, schemas

router = APIRouter()

@router.post("/like", response_model=schemas.Like)
def like_post(
	*,
	db: Session = Depends(get_db),
	user: models.User = Depends(get_current_user),
	post_id: int,
) -> Any:
	# Check if post exists and if it's not own post
	post = crud.post.get(db=db, id=post_id)
	if not post:
		raise HTTPException(404, "Post not found")
	if post.creator_id == user.id:
		raise HTTPException(403, "Can't like own posts")
		
	# Delete dislike if exitsts on this post by user
	dislike = crud.dislike.get(db=db, post_id=post_id, user_id=user.id)
	if dislike:
		crud.dislike.remove(db=db, id=dislike.id)

	# Add like
	like = crud.like.get(db=db, post_id=post_id, user_id=user.id)
	if not like:
		like_schema = schemas.LikeCreate(user_id=user.id, post_id=post_id)
		like = crud.like.create(db=db, obj_in=like_schema)
		return like
	else:
		raise HTTPException(409, "Like already exists")

@router.post("/dislike", response_model=schemas.Dislike)
def dislike_post(
	*,
	db: Session = Depends(get_db),
	user: models.User = Depends(get_current_user),
	post_id: int,
) -> Any:
	# Check if post exists and if it's not own post
	post = crud.post.get(db=db, id=post_id)
	if not post:
		raise HTTPException(404, "Post not found")
	if post.creator_id == user.id:
		raise HTTPException(403, "Can't dislike own posts")

	# Delete like if exitsts on this post by user
	like = crud.like.get(db=db, post_id=post_id, user_id=user.id)
	if like:
		crud.like.remove(db=db, id=like.id)

	# Add dislike
	dislike = crud.dislike.get(db=db, post_id=post_id, user_id=user.id)
	if not dislike:
		dislike_schema = schemas.DislikeCreate(user_id=user.id, post_id=post_id)
		dislike = crud.dislike.create(db=db, obj_in=dislike_schema)
		return dislike
	else:
		raise HTTPException(409, "Dislike already exists")

@router.delete("/like", response_model=schemas.Like)
def delete_like(
	*,
	db: Session = Depends(get_db),
	user: models.User = Depends(get_current_user),
	post_id: int,
) -> Any:
	like = crud.like.get(db=db, post_id=post_id, user_id=user.id)
	if not like:
		raise HTTPException(404, "Like not exists")
	else:
		like = crud.like.remove(db=db, id=like.id)
		return like

@router.delete("/dislike", response_model=schemas.Dislike)
def delete_dislike(
	*,
	db: Session = Depends(get_db),
	user: models.User = Depends(get_current_user),
	post_id: int,
) -> Any:
	dislike = crud.dislike.get(db=db, post_id=post_id, user_id=user.id)
	if not dislike:
		raise HTTPException(404, "Dislike not exists")
	else:
		dislike = crud.dislike.remove(db=db, id=dislike.id)
		return dislike