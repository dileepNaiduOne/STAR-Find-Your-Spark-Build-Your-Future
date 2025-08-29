from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, text
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.database.create_tables_structure import UserData

load_dotenv()  

DATABASE_URL = os.getenv("POSTGRESQL_ADDON_URI")
engine = create_engine(DATABASE_URL)


def ckeck_if_email_in_user_data(email):
    query = text("SELECT COUNT(*) FROM user_data WHERE email = :email")
    with engine.connect() as conn:
        result = conn.execute(query, {"email": email}).scalar()
        return result
    
SessionLocal = sessionmaker(bind=engine)

def add_new_user_to_user_data(name, email, age, gender, pin, secret_sentence):
    session = SessionLocal()
    try:
        new_user = UserData(user_name=name, email=email, age=age, gender=gender, pin=pin, secret_sentence=secret_sentence)
        session.add(new_user)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def ckeck_if_user_in_user_data(email, pin):
    query = text("SELECT * FROM user_data WHERE email = :email and pin =:pin")
    with engine.connect() as conn:
        result = conn.execute(query, {"email": email, "pin": pin})
        data = result.fetchall()
        if len(data) > 0:
            user = data[0]
        else:
            user = None
        return user
    
if __name__ == '__main__':
    pass