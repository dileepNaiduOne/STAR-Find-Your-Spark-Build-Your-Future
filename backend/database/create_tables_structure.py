from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

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

    profiles = relationship("ProfileData", back_populates="user")

class ProfileData(Base):
    __tablename__ = "profile_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user_data.user_id"), nullable=False)
    profile = Column(Text, nullable=False)
    soft_skills = Column(Text, nullable=False)
    tech_skills = Column(Text, nullable=False)

    user = relationship("UserData", back_populates="profiles")

Base.metadata.create_all(engine)
