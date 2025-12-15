import os
from dotenv import load_dotenv

# Load .env from current working directory
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")  # Must match exactly the .env variable

settings = Settings()
