from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Configure the database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./bookbuddy.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()