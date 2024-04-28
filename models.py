# models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    ratings = relationship("Rating", back_populates="user")
    discussions = relationship("Discussion", back_populates="user")

class Book(Base):
    __tablename__ = "books"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    description = Column(Text)
    ratings = relationship("Rating", back_populates="book")
    discussions = relationship("Discussion", back_populates="book")

class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    rating = Column(Integer)
    user = relationship("User", back_populates="ratings")
    book = relationship("Book", back_populates="ratings")

class Discussion(Base):
    __tablename__ = "discussions"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    content = Column(Text)
    user = relationship("User", back_populates="discussions")
    book = relationship("Book", back_populates="discussions")

# Pydantic models for data validation and serialization/deserialization
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    hashed_password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

class BookBase(BaseModel):
    title: str
    author: str
    description: str

class BookResponse(BookBase):
    id: int

class RatingBase(BaseModel):
    user_id: int
    book_id: int
    rating: int

class RatingResponse(RatingBase):
    id: int

class DiscussionBase(BaseModel):
    user_id: int
    book_id: int
    content: str

class DiscussionResponse(DiscussionBase):
    id: int
