from dotenv import load_dotenv
import os
import random

load_dotenv()  


def get_a_key():
    i = random.randint(1, 2)
    key = os.getenv(f"GOOGLE-API-KEY{i}")
    return key

if __name__ == "__main__":
    pass