from typing import Any

import crud
import models
import schemas
from deps import get_current_user, get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/post', response_model=schemas.Post)
def create_post(db: Session = Depends(get_db), user: models.User = Depends(get_current_user), *, post: schemas.PostBase):
	created_post = crud.post.create(db, post_in=post, user=user)
	return created_post

@router.get('/post/{post_id}', response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)) -> Any:
	post = crud.post.get(db, post_id)
	if not post:
		raise HTTPException(404, "Post not found")
	return post

@router.get('/posts', response_model=list[schemas.Post])
def read_posts(
	db: Session = Depends(get_db),
	user: models.User = Depends(get_current_user),
	skip: int = 0, 
	limit: int = 100
	):
	posts = crud.post.get_multi(db, skip=skip, limit=limit)
	if not posts:
		raise HTTPException(404, "Posts not found")
	return posts

@router.get('/posts/{user_id}', response_model=list[schemas.Post])
def read_user_posts(
	user_id: int, 
	db: Session = Depends(get_db), 
	user: models.User = Depends(get_current_user), 
	skip: int = 0, 
	limit: int = 100
	) -> Any:
	posts = crud.post.get_by_user(db, user_id=user_id, skip=skip, limit=limit)
	if not posts:
		raise HTTPException(404, "Posts not found")
	return posts

@router.put('/post/{id}', response_model=schemas.Post)
def update_post(
	*,
	id: int, 
	db: Session = Depends(get_db), 
	post_in: schemas.PostUpdate,
	user: models.User = Depends(get_current_user)
	) -> Any:
	"""
	Update post
	"""
	post = crud.post.get(db=db, id=id)
	if not post:
		raise HTTPException(404, "Post not found")
	if post.creator_id != user.id:
		raise HTTPException(400, "Not enough permission")
	post = crud.post.update(db=db, db_obj=post, obj_in=post_in)
	return post

@router.delete("/post/{id}", response_model=schemas.Post)
def delete_post(
	*,
	db: Session = Depends(get_db),
	id: int,
	user: models.User = Depends(get_current_user)
) -> Any:
	"""
	Delete post
	"""
	post = crud.post.get(db=db, id=id)
	if not post:
		raise HTTPException(404, "Post not found")
	if post.creator_id != user.id:
		raise HTTPException(400, "Not enough permission")
	post = crud.post.remove(db=db, id=id)
	return post


