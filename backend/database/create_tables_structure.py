from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

load_dotenv()  

DATABASE_URL = os.getenv("POSTGRESQL_ADDON_URI")

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class UserData(Base):
    __tablename__ = "user_data"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(100), nullable=False)
    pin = Column(String(4), nullable=False)
    secret_sentence = Column(String(300), nullable=False)

Base.metadata.create_all(engine)


# try:
#     with engine.connect() as conn:
#         conn.execute(text("SELECT current_database();"))
#         conn.commit()
#         print("✅ Table 'users' created (if not already).")
# except Exception as e:
#     print("❌ Error:", e)
