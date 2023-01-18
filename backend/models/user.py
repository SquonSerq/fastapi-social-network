from db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    # Possible to create superuser, not included in this project
    # is_superuser = Column(Boolean(), default=False)

    posts = relationship("Post",
    back_populates="creator",
    cascade="all, delete")
    likes = relationship("Like",
    back_populates="user",
    cascade="all, delete")
    dislikes = relationship("Dislike",
    back_populates="user",
    cascade="all, delete")