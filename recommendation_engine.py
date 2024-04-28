import pandas as pd
from surprise import Reader, Dataset, SVD
from sqlalchemy.orm import Session
from models import User, Book, Rating

def get_recommendations(user: User, db: Session, top_n=10):
    # Load data from the database
    ratings_data = db.query(Rating.user_id, Rating.book_id, Rating.rating).all()
    books_data = db.query(Book.id, Book.title, Book.author).all()

    # Convert data to pandas dataframes
    ratings_df = pd.DataFrame(ratings_data, columns=['user_id', 'book_id', 'rating'])
    books_df = pd.DataFrame(books_data, columns=['book_id', 'title', 'author'])

    # Create a reader for the surprise library
    reader = Reader(rating_scale=(1, 5))

    # Load data into a surprise dataset
    data = Dataset.load_from_df(ratings_df[['user_id', 'book_id', 'rating']], reader)

    # Split data into train and test sets
    trainset = data.build_full_trainset()

    # Train the SVD algorithm
    algo = SVD()
    algo.fit(trainset)

    # Get the user's past ratings
    user_ratings = ratings_df[ratings_df['user_id'] == user.id]

    # Get the user's rated book ids
    rated_book_ids = user_ratings['book_id'].tolist()

    # Get unrated books
    unrated_books = books_df[~books_df['book_id'].isin(rated_book_ids)]

    # Make predictions for unrated books
    predictions = []
    for _, book in unrated_books.iterrows():
        prediction = algo.predict(user.id, book['book_id'])
        predictions.append((book['book_id'], book['title'], book['author'], prediction.est))

    # Sort predictions by rating and return top_n
    sorted_predictions = sorted(predictions, key=lambda x: x[3], reverse=True)
    top_recommendations = sorted_predictions[:top_n]

    # Convert recommendations to Book objects
    recommended_books = []
    for book_id, title, author, rating in top_recommendations:
        book = db.query(Book).filter(Book.id == book_id).first()
        recommended_books.append(book)

    return recommended_books