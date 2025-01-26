from os import environ

from dotenv import load_dotenv

load_dotenv()

MOON_DREAM_API_KEY = environ.get("MOON_DREAM_API_KEY")
MOON_DREAM_MODEL_PATH = environ.get("MOON_DREAM_MODEL_PATH")
