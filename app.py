# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from typing import List
# from datetime import timedelta
#
# from models import Base, User, Book, Rating, Discussion, UserResponse
# from database import get_db, engine
# from authentication import authenticate_user, create_access_token, get_password_hash
# from recommendation_engine import get_recommendations
#
# app = FastAPI()
#
# Base.metadata.create_all(bind=engine)
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# @app.post("/token", response_model=dict)
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=30)
#     access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}
#
# # @app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# # async def create_user(user: User, db: Session = Depends(get_db)):
# #     existing_user = db.query(User).filter(User.username == user.username).first()
# #     if existing_user:
# #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
# #     user.hashed_password = get_password_hash(user.hashed_password)
# #     db.add(user)
# #     db.commit()
# #     db.refresh(user)
# #     return UserResponse.from_orm(user)
#
# @app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# async def create_user(user: User, db: Session = Depends(get_db)):
#     existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
#     if existing_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
#     user_db = UserDB(**user.dict())
#     user_db.hashed_password = get_password_hash(user_db.hashed_password)
#     db.add(user_db)
#     db.commit()
#     db.refresh(user_db)
#     return UserResponse.from_orm(user_db)
#
# @app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
# async def create_book(book: Book, db: Session = Depends(get_db)):
#     existing_book = db.query(Book).filter(Book.title == book.title, Book.author == book.author).first()
#     if existing_book:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists")
#     db.add(book)
#     db.commit()
#     db.refresh(book)
#     return book
#
# @app.get("/books", response_model=List[Book])
# async def get_books(db: Session = Depends(get_db)):
#     books = db.query(Book).all()
#     return books
#
# @app.get("/books/{book_id}", response_model=Book)
# async def get_book(book_id: int, db: Session = Depends(get_db)):
#     book = db.query(Book).filter(Book.id == book_id).first()
#     if not book:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
#     return book
#
# @app.post("/ratings", response_model=Rating, status_code=status.HTTP_201_CREATED)
# async def create_rating(rating: Rating, db: Session = Depends(get_db)):
#     existing_rating = db.query(Rating).filter(Rating.user_id == rating.user_id, Rating.book_id == rating.book_id).first()
#     if existing_rating:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating already exists")
#     db.add(rating)
#     db.commit()
#     db.refresh(rating)
#     return rating
#
# @app.get("/ratings/{user_id}", response_model=List[Rating])
# async def get_user_ratings(user_id: int, db: Session = Depends(get_db)):
#     ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
#     return ratings
#
# @app.get("/recommendations/{user_id}", response_model=List[Book])
# async def get_user_recommendations(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     recommendations = get_recommendations(user, db)
#     return recommendations
#
# @app.post("/discussions", response_model=Discussion, status_code=status.HTTP_201_CREATED)
# async def create_discussion(discussion: Discussion, db: Session = Depends(get_db)):
#     db.add(discussion)
#     db.commit()
#     db.refresh(discussion)
#     return discussion
#
# @app.get("/discussions/{book_id}", response_model=List[Discussion])
# async def get_book_discussions(book_id: int, db: Session = Depends(get_db)):
#     discussions = db.query(Discussion).filter(Discussion.book_id == book_id).all()
#     return discussions

# app.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from models import User, Book, Rating, Discussion, UserResponse, UserCreate, BookBase, BookResponse, RatingBase, RatingResponse, DiscussionBase, DiscussionResponse
from database import SessionLocal, engine  # Import Base and engine from database.py
from authentication import authenticate_user, create_access_token, get_password_hash
from recommendation_engine import get_recommendations

app = FastAPI()

# Base.metadata.create_all(bind=engine) # Moved this line to main

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Your endpoints and other functions...
@app.post("/clear_db", status_code=status.HTTP_204_NO_CONTENT)
def clear_db(db: Session = Depends(get_db)):
    try:
        # Delete all records from each table
        db.query(User).delete()
        db.query(Book).delete()
        db.query(Rating).delete()
        db.query(Discussion).delete()
        # Commit the transaction
        db.commit()
        return
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    hashed_password = get_password_hash(user.hashed_password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookBase, db: Session = Depends(get_db)):
    existing_book = db.query(Book).filter(Book.title == book.title, Book.author == book.author).first()
    if existing_book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists")
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books", response_model=List[BookResponse])
async def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@app.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@app.post("/ratings", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
async def create_rating(rating: RatingBase, db: Session = Depends(get_db)):
    existing_rating = db.query(Rating).filter(Rating.user_id == rating.user_id, Rating.book_id == rating.book_id).first()
    if existing_rating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating already exists")
    db_rating = Rating(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@app.get("/ratings/{user_id}", response_model=List[RatingResponse])
async def get_user_ratings(user_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
    return ratings

@app.get("/recommendations/{user_id}", response_model=List[BookResponse])
async def get_user_recommendations(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    recommendations = get_recommendations(user, db)
    return recommendations

@app.post("/discussions", response_model=DiscussionResponse, status_code=status.HTTP_201_CREATED)
async def create_discussion(discussion: DiscussionBase, db: Session = Depends(get_db)):
    db_discussion = Discussion(**discussion.dict())
    db.add(db_discussion)
    db.commit()
    db.refresh(db_discussion)
    return db_discussion

@app.get("/discussions/{book_id}", response_model=List[DiscussionResponse])
async def get_book_discussions(book_id: int, db: Session = Depends(get_db)):
    discussions = db.query(Discussion).filter(Discussion.book_id == book_id).all()
    return discussions
