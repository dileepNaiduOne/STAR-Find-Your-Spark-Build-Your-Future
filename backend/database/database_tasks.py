from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.database.create_tables_structure import UserData

# Load environment variables
load_dotenv()  

DATABASE_URL = os.getenv("POSTGRESQL_ADDON_URI")

# Configure engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=5,          # max 5 connections in pool
    max_overflow=0,       # don’t allow more than 5
    pool_timeout=30,      # wait 30s before raising error
    pool_recycle=1800     # recycle connections every 30 min
)

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def check_if_email_in_user_data(email: str):
    """Check if an email exists in user_data table."""
    session = SessionLocal()
    try:
        query = text("SELECT COUNT(*) FROM user_data WHERE email = :email")
        result = session.execute(query, {"email": email}).scalar()
        return result
    finally:
        session.close()  # return connection to pool


def add_new_user_to_user_data(name, email, age, gender, pin, secret_sentence):
    """Add a new user to user_data table."""
    session = SessionLocal()
    try:
        new_user = UserData(
            user_name=name,
            email=email,
            age=age,
            gender=gender,
            pin=pin,
            secret_sentence=secret_sentence
        )
        session.add(new_user)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def check_if_user_in_user_data(email: str, pin: str):
    """Check if a user exists with given email and pin."""
    session = SessionLocal()
    try:
        query = text("SELECT * FROM user_data WHERE email = :email AND pin = :pin")
        result = session.execute(query, {"email": email, "pin": pin})
        data = result.fetchall()
        return data[0] if data else None
    finally:
        session.close()


if __name__ == '__main__':
    pass
