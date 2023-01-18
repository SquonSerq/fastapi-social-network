from db.base_class import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    post_text = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post")
    dislikes = relationship("Dislike", back_populates="post")

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")

class Dislike(Base):
    __tablename__ = "dislikes"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    post = relationship("Post", back_populates="dislikes")
    user = relationship("User", back_populates="dislikes")
