# test_db.py
import os
from dotenv import load_dotenv

load_dotenv()

def test_database_url():
    DATABASE_URL = os.getenv("DATABASE_URL")
    print(f"DATABASE_URL from .env: {DATABASE_URL}")
    
    if DATABASE_URL:
        if DATABASE_URL.startswith("postgres://"):
            fixed_url = DATABASE_URL.replace("postgres://", "postgresql://", 1)
            print(f"Fixed URL: {fixed_url}")
        else:
            print("URL format is correct")
    else:
        print("Using local database")
        print("Local URL: postgresql://postgres:Admin123@localhost:5432/businessconnect")

if __name__ == "__main__":
    test_database_url()