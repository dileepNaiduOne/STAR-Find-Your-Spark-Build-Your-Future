from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()  

DATABASE_URL = os.getenv("POSTGRESQL_ADDON_URI")

engine = create_engine(DATABASE_URL)

# Open connection
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM USER_DATA;"))
    print(result.fetchall())
