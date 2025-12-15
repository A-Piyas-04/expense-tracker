import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env automatically

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://expense_user:expense_pass@db:5433/expense_db")

settings = Settings()

# Optional sanity check
if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please define it in .env")
