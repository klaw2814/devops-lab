import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "DevOps Lab API")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    DATABASE_URL = os.getenv(
    	"DATABASE_URL",
    	"sqlite:///./tickets.db"
	)

settings = Settings()
