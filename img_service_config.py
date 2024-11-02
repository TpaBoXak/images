import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.service")

class Config:
    RABBITMQ_URL = os.getenv("RABBITMQ_URL")

    IMAGES_FOLDER = Path(os.getenv("IMAGES_FOLDER"))

    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

    IMAGE_SIZE = (500, 500)

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
settings = Config()

print(settings.RABBITMQ_URL, settings.IMAGES_FOLDER)