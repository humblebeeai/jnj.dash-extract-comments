import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")

# App Settings
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
APP_TITLE = "Excel Data Extraction Dashboard"
MAX_ROWS_PREVIEW = 20
